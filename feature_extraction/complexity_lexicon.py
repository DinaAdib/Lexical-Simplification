import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from files_paths import *
#{ Part-of-speech constants
ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
#}
POS_LIST = [NOUN, VERB, ADJ, ADV]

class WordComplexityLexicon:
    def __init__(self):
        self.word_complexity = {}
        for line in open(COMPLEXITY_LEXICON_PATH):
            tokens = [t.strip() for t in line.strip().split('\t')]
            self.word_complexity[tokens[0].lower()] = float(tokens[1])
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()

    def get_feature(self, phrase):
        # take the longest word if given a phrase
        print("here")
        if len(phrase.split()) > 1:
            word = max(phrase, key=len)
        else:
            word = phrase

        if word in self.word_complexity.keys():
            return [self.word_complexity[word], 1.0]
        else:
            print("here")
            complexities = []
            # lemmatized noun
            lemmatized_word_noun = self.lemmatizer.lemmatize(word)
            if lemmatized_word_noun in self.word_complexity.keys():
                complexities.append(self.word_complexity[lemmatized_word_noun])
            # lemmatized verb
            lemmatized_word_verb = self.lemmatizer.lemmatize(word, pos='v')
            if lemmatized_word_verb in self.word_complexity.keys():
                complexities.append(self.word_complexity[lemmatized_word_verb])
            # lemmatized adverb
            lemmatized_word_adj = self.lemmatizer.lemmatize(word, pos='a')
            if lemmatized_word_adj in self.word_complexity.keys():
                complexities.append(self.word_complexity[lemmatized_word_adj])
            # lemmatized noun
            lemmatized_word_adv = self.lemmatizer.lemmatize(word, pos='r')
            if lemmatized_word_adv in self.word_complexity.keys():
                complexities.append(self.word_complexity[lemmatized_word_adv])


            stemmed_word = self.stemmer.stem(word)
            if stemmed_word in self.word_complexity.keys() and abs(len(stemmed_word) - len(word)) <= 4:
                complexities.append(self.word_complexity[stemmed_word])
            print(lemmatized_word_adv, lemmatized_word_adj, lemmatized_word_verb,lemmatized_word_noun, stemmed_word)
            print(complexities)

            if len(complexities) > 0:
                return [max(complexities), 1.0]
        return [0.0,0.0]