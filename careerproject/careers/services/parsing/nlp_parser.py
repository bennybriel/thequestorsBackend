import spacy
from typing import Dict, Any
from .base_parser import BaseParser

class NLPParser(BaseParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def parse(self, raw_input: str) -> Dict[str, Any]:
        doc = self.nlp(raw_input)
        
        result = {
            'hobbies': self._extract_entities(doc, ['HOBBY']),
            'passions': self._extract_entities(doc, ['PASSION']),
            'favorite_activities': self._extract_phrases(doc, ['love', 'enjoy']),
            'vision': self._extract_sentences(doc, ['vision', 'goal']),
            'dream': self._extract_sentences(doc, ['dream', 'aspiration'])
        }
        
        return result
    
    def _extract_entities(self, doc, labels):
        return [ent.text for ent in doc.ents if ent.label_ in labels]
    
    def _extract_phrases(self, doc, triggers):
        phrases = []
        for token in doc:
            if token.text.lower() in triggers:
                phrases.append(' '.join([t.text for t in token.subtree]))
        return phrases
    
    def _extract_sentences(self, doc, triggers):
        return ' '.join([sent.text for sent in doc.sents 
                       if any(trigger in sent.text.lower() for trigger in triggers)])