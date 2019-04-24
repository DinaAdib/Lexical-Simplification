import numpy as np
from files_paths import *
from feature_extraction.complexity_lexicon import *

class FeatureExtractor:
    def __init__(self):
        self.word_lexicon = WordComplexityLexicon()

    def get_features(self,tain=False):
        for file in TRAINING_FILES:
            for line in open(file):
                tokens = line.strip().split('\t')
                sentence = tokens[0].strip()
                complex_word = tokens[1].strip()
                ranks = [int(token.strip().split(':')[0]) for token in tokens[3:]]
                candidates = [token.strip().split(':')[1] for token in tokens[3:]]
                features = FeatureExtractor.get_single_features(self, candidates, complex_word)

    def get_single_features(self, candidates, complex_word):
        features = {}
        candidate_features = []
        for candidate in candidates:
            candidate_features.append(len(candidate.split())) # number of words
            candidate_features.append(len(candidate)) # number of characters
            candidate_features.extend(self.word_lexicon.get_feature(candidate))

fe = FeatureExtractor()
fe.get_features()