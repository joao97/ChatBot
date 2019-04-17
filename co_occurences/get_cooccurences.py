from word_cloud import utils
import pandas as pd
import numpy as np
import nltk
from PIL import Image
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re


def get_cooccurences(characters, scripts, top):

    #characters_name = list(set(characters_name))
    characters_name = [character.lower().split(' ')[0] for character in characters_name if character.lower().split(' ')[0] not in STOPWORDS]
        
    #tokenizing all the text
    counter = []
    characters = []
    for episode, script in scripts.items():
        for line in script:
            if line[1]=='Scene Change':
                characters = list(set(characters))
                [counter.append([characters[i], characters[j], 1]) for i in range(len(characters)) for j in range(i+1, len(characters))]
                characters=[]
            elif line[1]=='Phrase':
                found_characters = re.search('(\w{2,}(\s\w{2,})?)(.*)?\:', line[0].lower()).group(1)
                if found_characters in characters_name:
                    characters.append(found_characters)
    
    counting = pd.DataFrame(counter, columns = ['char1', 'char2', 'count'])
    counting = counting.groupby(by=['char1','char2']).sum().reset_index()
    
    return counting.sort_values(by='count', ascending=False).head(top)
