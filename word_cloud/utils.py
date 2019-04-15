import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import contractions
import re

#normalization
def normalize(tokens):
    #remove punctuation tokens and special characters
    tokens = [re.sub(r'[^\w\s]|_','',token).lower() for token in tokens if not re.match('^\.{3}|[^\w\s\d]$',token)]
    #removing stopwords
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in tokens:
        if w!='' and w not in stop_words:
            filtered_sent.append(w)
    return filtered_sent

#method to handle with the different types of words, such as, names, verbs or adjectives
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def lemmatize(tokens):
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token, pos=get_wordnet_pos(token)) for token in tokens]
    return tokens


def preprocessing(text):
    text = contractions.fix(text)
    return lemmatize(normalize(nltk.word_tokenize(text)))