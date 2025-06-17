from transformers import pipeline
from django.conf import settings

class HobbyClassifier:
    def __init__(self):
        # In production, we would load a fine-tuned model
        self.classifier = pipeline(
            "text-classification",
            model="bert-base-uncased",
            tokenizer="bert-base-uncased"
        )
        self.categories = {
            'ART': 'Arts & Creativity',
            'TECH': 'Technology',
            'OUT': 'Outdoor',
            'SOC': 'Social',
            'SPORT': 'Sports',
            'GAME': 'Gaming',
            'READ': 'Reading',
            'MUSIC': 'Music',
            'OTHER': 'Other'
        }

    def classify_hobbies(self, hobbies_text):
        # Simple implementation - in production would use proper model
        results = self.classifier(hobbies_text)
        top_categories = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
        return [label['label'] for label in top_categories]