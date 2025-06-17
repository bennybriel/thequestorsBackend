import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch
from django.conf import settings
from careers.models import Career
from users.models import CustomUser
from .models import CareerMatch
from celery import shared_task
from django.core.cache import cache

class CareerPredictorService:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = BertModel.from_pretrained('bert-base-uncased')
        self.bert_model.eval()  # Set to evaluation mode

        # Pre-load career embeddings
        self.career_embeddings = {}
        self.load_career_embeddings()

    def load_career_embeddings(self):
        """Pre-load or compute embeddings for all careers"""
        careers = Career.objects.all()
        for career in careers:
            career_text = f"{career.title} {career.description} {' '.join(career.required_skills)}"
            self.career_embeddings[career.id] = self.get_embedding(career_text)

    def get_embedding(self, text):
        """Convert text to embedding vector using BERT"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def predict_careers(self, user_id):
        """Main prediction method"""
        user = CustomUser.objects.get(pk=user_id)
        profile = user.profile

        # Process user inputs
        user_text = f"{profile.hobbies} {profile.happy_activities} {profile.personal_vision} {' '.join(user.skills)}"
        user_embedding = self.get_embedding(user_text)

        # Compare with all careers
        matches = []
        for career_id, career_embedding in self.career_embeddings.items():
            career = Career.objects.get(pk=career_id)

            # Calculate similarity
            similarity = cosine_similarity([user_embedding], [career_embedding])[0][0]
            match_score = (similarity + 1) * 50  # Convert to 0-100 scale

            # Calculate skill matches and gaps
            user_skills = set(user.skills)
            required_skills = set(career.required_skills)
            skill_match = list(user_skills.intersection(required_skills))
            skill_gaps = list(required_skills.difference(user_skills))

            matches.append({
                'career': career,
                'score': match_score,
                'skill_match': skill_match,
                'skill_gaps': skill_gaps,
                'explanation': self.generate_explanation(match_score, skill_match, skill_gaps)
            })

        # Sort and return top matches
        sorted_matches = sorted(matches, key=lambda x: x['score'], reverse=True)
        return sorted_matches[:10]

    def generate_explanation(self, score, skill_match, skill_gaps):
        """Generate human-readable explanation for the match"""
        if score > 80:
            base = "Excellent match! "
        elif score > 60:
            base = "Good match. "
        else:
            base = "Potential match worth exploring. "

        if skill_match:
            base += f"You have {len(skill_match)} of the key required skills. "
        if skill_gaps:
            base += f"You would need to develop {len(skill_gaps)} additional skills. "

        return base.strip()

@shared_task(bind=True)
def predict_careers_task(self, user_id):
    """Celery task for async prediction"""
    try:
        predictor = CareerPredictorService()
        matches = predictor.predict_careers(user_id)

        # Save results
        user = CustomUser.objects.get(pk=user_id)
        CareerMatch.objects.filter(user=user).delete()

        saved_matches = []
        for match in matches:
            cm = CareerMatch.objects.create(
                user=user,
                career=match['career'],
                match_score=match['score'],
                skill_match=match['skill_match'],
                skill_gaps=match['skill_gaps'],
                explanation=match['explanation']
            )
            saved_matches.append(cm)

        # Cache results
        cache_key = f"user_{user_id}_matches"
        cache.set(cache_key, [cm.id for cm in saved_matches], timeout=3600*24)

        return {"status": "success", "matches": len(saved_matches)}
    except Exception as e:
        self.retry(exc=e, countdown=60, max_retries=3)