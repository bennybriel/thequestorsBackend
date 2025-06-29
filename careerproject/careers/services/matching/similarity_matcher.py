from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Any
from ...models.career import CareerPath
from rest_framework.exceptions import APIException

class SimilarityMatcher:
    MIN_SIMILARITY_THRESHOLD = 0.2
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.career_paths = list(CareerPath.objects.all())
        if not self.career_paths:
            raise APIException("No career paths available in database")
        self._train_vectorizer()
    
    def match(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        self._validate_user_data(user_data)
        user_text = self._create_user_text(user_data)
        user_vector = self.vectorizer.transform([user_text])
        
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)
        sorted_indices = np.argsort(similarities[0])[::-1]
        
        return [
            self._format_match_result(i, similarities[0][i])
            for i in sorted_indices
            if similarities[0][i] >= self.MIN_SIMILARITY_THRESHOLD
        ][:5]  # Return top 5 matches
    
    def _validate_user_data(self, user_data: Dict[str, Any]):
        if not isinstance(user_data, dict):
            raise ValueError("User data must be a dictionary")
            
        if not any(key in user_data for key in ['hobbies', 'passions', 'vision', 'dream']):
            raise ValueError("User data missing required fields")
    
    def _create_user_text(self, user_data: Dict[str, Any]) -> str:
        return ' '.join([
            ' '.join(user_data.get('hobbies', [])),
            ' '.join(user_data.get('passions', [])),
            user_data.get('vision', ''),
            user_data.get('dream', '')
        ])
    
    def _train_vectorizer(self):
        documents = [
            f"{path.title} {' '.join(path.required_skills)} {path.description} {path.industry}"
            for path in self.career_paths
        ]
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
    
    def _format_match_result(self, index: int, score: float) -> Dict[str, Any]:
        path = self.career_paths[index]
        return {
            'id': path.id,
            'title': path.title,
            'description': path.description,
            'match_score': float(score),
            'required_skills': path.required_skills[:5],  # Show top 5 skills
            'salary_range': path.salary_range,
            'industry': path.industry
        }