# @InProceedings{pavlick-EtAl:2016:ACL,
#   author    = {Pavlick, Ellie and  Callison-Burch, Chris},
#   title     = {Simple PPDB: A Paraphrase Database for Simplification},
#   booktitle = {Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Short Papers)},
#   month     = {August},
#   year      = {2016},
#   address   = {Berlin, Germany},
#   publisher = {Association for Computational Linguistics},
# }

from files_paths import *
import numpy as np
import pickle
import nltk
from nltk.corpus import wordnet as wn

sppdb_score_file = CURRENT_DIRECTORY_PATH + "/simplification-dictionary"
BenchLS_file = CURRENT_DIRECTORY_PATH + "BenchLS.txt"
BenchPS_file = CURRENT_DIRECTORY_PATH + "/BenchPS.txt"
common20LS_file = CURRENT_DIRECTORY_PATH + "/Common20LS.txt"
words_quality_score_cutoff = 3.5
phrase_quality_score_cutoff = 4
simplification_score_cutoff = 0.75

def get_simplification_dictionary():
    ppdb_substitutions = {}
    for line in open(sppdb_score_file):
        # paraphraseScore   SimplificationScore    SynacticCategory    InputPhrase    OutputPhrase
        tokens = [t.strip().lower() for t in line.strip().split('\t')]
        quality_cutoff = words_quality_score_cutoff
        if len(tokens[3].split()) > 1 or len(tokens[4].split()) > 1:
            quality_cutoff = phrase_quality_score_cutoff
        if float(tokens[0]) > quality_cutoff and  float(tokens[1]) > simplification_score_cutoff:
            if tokens[3] in ppdb_substitutions.keys():
                ppdb_substitutions[tokens[3]] = {tokens[4]:{"pos":tokens[2], "ppdbscore":tokens[0], "nrep": 1}}
            else:
                ppdb_substitutions[tokens[3]] = {}
                ppdb_substitutions[tokens[3]] = {tokens[4]:{"pos":tokens[2], "ppdbscore":tokens[0], "nrep": 1}}

    print(len(ppdb_substitutions))
    save_obj(ppdb_substitutions,"substitutions")
    return substitutions

def get_BenchLS_Candidates(substitutions):
    print(len(substitutions))
    for line in open(BenchLS_file):
        # Sentence   ComplexWord    Position    <rank_1>:<candidate_substitution_1> ... <rank_n>:<candidate_substitution_n>
        # Lower rank -> simpler word
        tokens = [t.strip().lower() for t in line.strip().split('\t')]
        if tokens[1] in substitutions.keys():
            # print("##########")
            # print(len(substitutions[tokens[1]]))

            subsitutes = [[index, np.array(substitute[0:2])] for index, substitute in enumerate(substitutions[tokens[1]])]
            # print(np.array(subsitutes).flatten())
            index = subsitutes[0]
            for token in tokens[3:]:
                if token in substitutions[tokens[1]].keys():
                    substitutions[tokens[1]][token[2:]]['nrep'] += 1
                else:
                    substitutions[tokens[1]][token[2:]] = {'pos':'[x]', 'nrep': 1}

            # print(len(substitutions[tokens[1]]))
        else:
            substitutions[tokens[1]] = [(tokens[3][2:], "[x]")]
            if len(tokens) > 3:
                for token in tokens[4:]:
                    if (token[2:],"[x]") not in substitutions[tokens[1]]:
                        substitutions[tokens[1]].append((token[2:], "[x]"))
                    # else:
        #                 print("Element found already")
        # print(tokens[1])
        # print(substitutions[tokens[1]])

    print(len(substitutions))

def get_common20LS_Candidates(substitutions):
    print(len(substitutions))
    for line in open(common20LS_file):
        # Sentence   ComplexWord    Position    <rank_1>:<candidate_substitution_1> ... <rank_n>:<candidate_substitution_n>
        # Lower rank -> simpler word
        tokens = [t.strip().lower() for t in line.strip().split('\t')]
        print(tokens)
        # if tokens[8] in substitutions.keys():
        #     # print("##########")
        #     # print(len(substitutions[tokens[1]]))
        #     for token in tokens[3:]:
        #         if (token[2:],"[x]") not in substitutions[tokens[1]]:
        #             substitutions[tokens[1]].append((token[2:], "[x]"))
        #         # else:
        #         #     print("Element found already")
        #
        #     # print(len(substitutions[tokens[1]]))
        # else:
        #     substitutions[tokens[8]] = [(tokens[3][2:], "[x]")]
        #     if len(tokens) > 3:
        #         for token in tokens[4:]:
        #             if (token[2:],"[x]") not in substitutions[tokens[1]]:
        #                 substitutions[tokens[1]].append((token[2:], "[x]"))
                    # else:
        #                 print("Element found already")
        # print(tokens[1])
        # print(substitutions[tokens[1]])

    print(len(substitutions))

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def wordnet_synonyms(word, pos):
    synset = wn.synsets(word, pos)

    print(synset)
    # return synonym lemmas in no particular order
    return [lemma.name() for s in synset for lemma in s.lemmas()]

def get_candidates(complex_word, complex_pos, substitutions):
    candidates = []
    if complex_word not in substitutions.keys():
        return candidates
    for substitute in substitutions[complex_word]:
        print(substitute)
        if complex_pos == substitutions[complex_word][substitute]['pos'] or substitutions[complex_word][substitute]['pos'] == '[x]':
            candidates.append(substitute)
    return candidates

# for testing
substitutions = load_obj("substitutions")
print(substitutions)
print(get_candidates("educational opportunity", "[np]", substitutions))
