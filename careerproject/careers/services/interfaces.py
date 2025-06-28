from abc import ABC, abstractmethod
from typing import Dict, List, Any

class IInputParser(ABC):
    @abstractmethod
    def parse(self, raw_input: str) -> Dict[str, Any]:
        pass

class ICareerMatcher(ABC):
    @abstractmethod
    def match(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

class IPlanGenerator(ABC):
    @abstractmethod
    def generate(self, career_path_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class IPdfGenerator(ABC):
    @abstractmethod
    def generate_pdf(self, plan_data: Dict[str, Any]) -> bytes:
        pass