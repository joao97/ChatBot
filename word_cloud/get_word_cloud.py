from word_cloud import utils
import pandas as pd
import numpy as np
import nltk
from PIL import Image
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import random


#loading the characters dataset to a dictionary
with open("data/characters.json") as f:
    data = json.load(f)

#selecting only the name of characters
characters_tokens = []
characters_name = []
for character in data['characters']:
    [characters_tokens.append(token) for token in utils.preprocessing(character['characterName'].lower())]
    characters_name.append(character['characterName'].lower())
    
characters_tokens = list(set(characters_tokens))

characters_name.remove('will') 
characters_name.remove('lady') 
characters_name.remove('ros') 

#loading the scripts
episode_script = np.load('data/processed_scripts.npy').item()

#tokenizing all the text
words = []
words_characters = []
for episode, script in episode_script.items():
    for line in script:
        if line[1]=='Phrase':
            tokens = utils.preprocessing(line[0])
            [words.append(token) for token in tokens]
            for character in characters_name:
                if character in line[0].lower():
                    words_characters.append(character)
            
#removing characters' names from the words            
words_no_characters = [word for word in words if word not in characters_tokens]

#extracting only the characters' names

#joining all the words
words = ' '.join(words)
words_no_characters = ' '.join(words_no_characters)         
words_characters = ' '.join(words_characters)


from collections import Counter
word_could_dict=Counter(words_characters)

#defining the masks
map_mask = np.array(Image.open("word_cloud/westeros_map.png"))
throne_mask = np.array(Image.open("word_cloud/ironthrone.png"))
sword_mask = np.array(Image.open("word_cloud/sword.png"))
  

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

#creating the wordcloud  
wc = WordCloud(width = 1000, height = 1000, background_color="white", max_words=100, mask=map_mask)    
wc.generate(words)
wc.to_file("word_cloud/words_wc_map.png")

wc = WordCloud(width = 1000, height = 1000, background_color="white", max_words=100, mask=map_mask)    
wc.generate(words_no_characters)
wc.to_file("word_cloud/no_characters_wc_map.png")

wc = WordCloud(width = 1000, height = 1000, background_color="white", max_words=100, mask=map_mask)    
wc.generate(words_characters)
wc.to_file("word_cloud/characters_wc_map.png")





wc = WordCloud(width = 1000, height = 1000, background_color="black", max_words=100, mask=sword_mask)    
wc.generate(words)
wc.recolor(color_func=grey_color_func, random_state=3)
wc.to_file("word_cloud/words_wc_sword2.png")

wc = WordCloud(width = 1000, height = 1000, background_color="black", max_words=100, mask=sword_mask)    
wc.generate(words_no_characters)
wc.recolor(color_func=grey_color_func, random_state=3)
wc.to_file("word_cloud/no_characters_wc_sword2.png")

wc = WordCloud(width = 1000, height = 1000, background_color="black", max_words=100, mask=sword_mask)    
wc.generate_from_frequencies(word_could_dict)
wc.recolor(color_func=grey_color_func, random_state=3)
wc.to_file("word_cloud/characters_wc_sword2.png")





wc = WordCloud(width = 1000, height = 1000, background_color="white", max_words=100, mask=throne_mask)    
wc.generate(words)
wc.to_file("word_cloud/words_wc_throne.png")

wc = WordCloud(width = 1000, height = 1000, background_color="white", max_words=100, mask=throne_mask)    
wc.generate(words_no_characters)
wc.to_file("word_cloud/no_characters_wc_throne.png")

wc = WordCloud(width = 1000, height = 1000, background_color="white", max_words=100, mask=throne_mask)    
wc.generate(words_characters)
wc.to_file("word_cloud/characters_wc_throne.png")
