import nltk
from nltk.corpus import wordnet


def get_synonyms(word, pos):
    syn = set()
    for synset in wordnet.synsets(word):
        if(synset.pos() == pos):
            for lemma in synset.lemmas():
                syn.add(lemma.name())  # add the synonyms
    synonyms = syn
    return synonyms


print(get_synonyms("make", 'v'))
