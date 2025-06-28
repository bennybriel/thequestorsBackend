from abc import ABC, abstractmethod
from typing import Dict, Any
from ..interfaces import IInputParser

class BaseParser(IInputParser, ABC):
    @abstractmethod
    def parse(self, raw_input: str) -> Dict[str, Any]:
        pass