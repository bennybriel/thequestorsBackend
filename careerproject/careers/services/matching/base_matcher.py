from abc import ABC, abstractmethod
from typing import Dict, List, Any
from ..interfaces import ICareerMatcher

class BaseMatcher(ICareerMatcher, ABC):
    @abstractmethod
    def match(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass