import spacy
from typing import Dict, Any
from rest_framework.exceptions import ValidationError

class NLPParser:
    MIN_INPUT_LENGTH = 10
    MAX_INPUT_LENGTH = 1000
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise ImportError("English language model not found. Run: python -m spacy download en_core_web_sm")
        
    def parse(self, raw_input: str) -> Dict[str, Any]:
        self._validate_input(raw_input)
        doc = self.nlp(raw_input)
        
        return {
            'hobbies': self._extract_entities(doc, ['HOBBY']),
            'passions': self._extract_phrases(doc, ['love', 'passionate about']),
            'favorite_activities': self._extract_phrases(doc, ['enjoy', 'like to']),
            'vision': self._extract_sentences(doc, ['vision', 'goal']),
            'dream': self._extract_sentences(doc, ['dream', 'aspiration']),
            'raw_input': raw_input
        }
    
    def _validate_input(self, raw_input: str):
        if not isinstance(raw_input, str):
            raise ValidationError("Input must be a string")
            
        if len(raw_input) < self.MIN_INPUT_LENGTH:
            raise ValidationError(f"Input must be at least {self.MIN_INPUT_LENGTH} characters")
            
        if len(raw_input) > self.MAX_INPUT_LENGTH:
            raise ValidationError(f"Input exceeds maximum length of {self.MAX_INPUT_LENGTH} characters")
    
    def _extract_entities(self, doc, labels):
        return [ent.text for ent in doc.ents if ent.label_ in labels]
    
    def _extract_phrases(self, doc, triggers):
        return [' '.join([t.text for t in sent]) 
               for sent in doc.sents 
               if any(trigger in sent.text.lower() for trigger in triggers)]
    
    def _extract_sentences(self, doc, triggers):
        return ' '.join([sent.text for sent in doc.sents 
                        if any(trigger in sent.text.lower() for trigger in triggers)])