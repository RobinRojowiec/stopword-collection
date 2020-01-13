"""

IDE: PyCharm
Project: corpus-analysis
Author: Robin
Filename: analyze
Date: 13.01.2020

"""
import spacy

from util import load_dict
from paths import DIAGRAMS, DICTS
import re
import numpy as np
import matplotlib.pyplot as plt
import math
from tqdm import tqdm

# analyze quality
nlp = spacy.load("de_core_news_sm")
total_frequency: dict = load_dict(DICTS + '/total_frequency.json')
document_frequency: dict = load_dict(DICTS + '/document_frequency.json')
total_docs = 10000
max_freq = sum(list(item[1] for item in total_frequency.items()))


# visualize
def count_bar_chart(counts, title):
    data: [] = list(counts.items())
    data.sort(key=lambda x: x[1], reverse=True)
    data = data[:20]

    objects = [x[0] for x in data]
    y_pos = np.arange(len(objects))
    performance = [x[1] / total_docs for x in data]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation='vertical')
    plt.ylabel('relative frequency')
    plt.title(title)

    plt.savefig(DIAGRAMS + '/' + title.replace(' ', '_').lower() + ".png", format='png')
    plt.clf()


count_bar_chart(total_frequency, "Total frequency")
count_bar_chart(document_frequency, "Document frequency")

# generate lists
dfs: [] = list([item[0], item[1]] for item in document_frequency.items())

word_pattern = re.compile('\\w+', flags=re.IGNORECASE)
dfs = list(filter(lambda x: word_pattern.match(x[0]), dfs))

# calculate information score
max_stop_words = 0
for token_df in tqdm(dfs):
    # token_df[1] = (total_frequency[token_df[0]]/max_freq)*math.log(total_docs / token_df[1])
    token_df[1] = math.log(total_docs / token_df[1])
    # token_df[1] = document_frequency[token_df[0]]#/max_freq

    if nlp(token_df[0])[0].is_stop:
        max_stop_words += 1

dfs.sort(key=lambda x: x[1], reverse=False)

dfreq_list = [x[1] for x in dfs]
print("Max: %.05f, Min: %.05f, Median:%.05f " % (max(dfreq_list), min(dfreq_list), np.median(dfreq_list)))

limit = 200
stopword_list = [token_df[0] for token_df in dfs[:limit]]

correct = 0
total = 0.0
for stopword in stopword_list:
    word = nlp(stopword)
    if word[0].is_stop:
        correct += 1
    total += 1

with open(DICTS + '/stopword_list_ger.dict', 'w+', encoding='utf-8') as dict_file:
    for word in stopword_list:
        dict_file.write(word + '\n')
print("Total Stopwords: %i, Accuracy: %.02f, Recall: %.02f" % (total, correct / total, correct / max_stop_words))
