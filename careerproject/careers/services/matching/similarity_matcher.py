from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Any
from ...models.career import CareerPath
from .base_matcher import BaseMatcher

class SimilarityMatcher(BaseMatcher):
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.career_paths = list(CareerPath.objects.all())
        self._train_vectorizer()
    
    def _train_vectorizer(self):
        documents = [
            f"{path.title} {' '.join(path.required_skills)} {path.description} {path.industry}"
            for path in self.career_paths
        ]
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
    
    def match(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        user_text = ' '.join([
            ' '.join(user_data.get('hobbies', [])),
            ' '.join(user_data.get('passions', [])),
            user_data.get('vision', ''),
            user_data.get('dream', '')
        ])
        
        user_vector = self.vectorizer.transform([user_text])
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)
        sorted_indices = np.argsort(similarities[0])[::-1]
        
        return [
            {
                'id': self.career_paths[i].id,
                'title': self.career_paths[i].title,
                'match_score': float(similarities[0][i]),
                'description': self.career_paths[i].description
            }
            for i in sorted_indices[:3]  # Return top 3 matches
        ]