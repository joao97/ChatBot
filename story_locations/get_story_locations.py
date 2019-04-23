import pandas as pd
import numpy as np
import nltk
import re
import json 
from scripts_processing import utils
import seaborn as sns
import matplotlib.pyplot as plt

#loading the scripts
episode_script = np.load('data/processed_scripts.npy').item()

#loading the characters dataset to a dictionary
with open("data/locations.json") as f:
    data = json.load(f)

#selecting only the name fo characters
regions = []
for region in data['regions']:
    for subregion in region['subLocation']:
        if subregion != '':
            regions.append([region['location'].lower().replace("'",''), subregion.lower().replace("'",'')])

#function to extract location from description
def find_regions(sentence, regions):
    for region in regions:
        if region[0] in sentence.lower().replace("'",''):
            return region[0]
        elif region[1] in sentence.lower().replace("'",''):
            if region[1]=='inn':
                return region[0]
            else:
                return region[1]
    return 'somewhere'

#finding locations
last_location = 'unknown'
counter = []
for episode, script in episode_script.items():
    for line in script:
        if line[1]=='Scene Change' or line[1]=='Description':
            if find_regions(line[0].lower(), regions) != 'somewhere':
                last_location = find_regions(line[0].lower(), regions)
        else:
            counter.append([episode,last_location, 1])
                

counter = pd.DataFrame(counter, columns = ['season','location','count'])

counter = pd.DataFrame(counter, columns = ['season','location','count'])


top5 = pd.DataFrame(counter.groupby('location').count().sort_values('count')['count'].tail(5))




fig , ax= plt.subplots()
plt.bar(top5.index, top5['count'], color='white')
plt.xlabel('Locations', color='white')
plt.ylabel('Frequency', color='white')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

fig.savefig('location_exploration.png', transparent=True)
