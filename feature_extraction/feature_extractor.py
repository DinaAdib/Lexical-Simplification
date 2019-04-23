import numpy as np
from .complexity_lexicon import *

class feature_extractor:
    def __init__(self):
        self.word_lexicon = WordComplexityLexicon()

    def get_features(self, ):
