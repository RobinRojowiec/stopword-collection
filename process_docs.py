"""

IDE: PyCharm
Project: corpus-analysis
Author: Robin
Filename: process_docs.py
Date: 12.01.2020

"""
from collections import defaultdict
from os import listdir

import spacy
from os.path import isfile, join
from tqdm import tqdm

from paths import LEIPZIG_DATA_DOCS, DICTS
from util import save_dict

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("de_core_news_sm")

leipzig_docs = [f for f in listdir(LEIPZIG_DATA_DOCS) if isfile(join(LEIPZIG_DATA_DOCS, f))]
leipzig_docs = leipzig_docs

# create indices
total_docs = len(leipzig_docs)
total_frequency = defaultdict(int)
document_frequency = defaultdict(int)

# collect statistics
for doc in tqdm(leipzig_docs):
    with open(LEIPZIG_DATA_DOCS + '/' + doc, 'r', encoding='utf-8') as text_file:
        text = text_file.read()
        spacy_doc = nlp(text)

        single_tokens = set()
        for token in spacy_doc:
            if token.is_alpha:
                total_frequency[token.text] += 1
                single_tokens.add(token.text)

        for st in single_tokens:
            document_frequency[st] += 1

save_dict(DICTS + '/document_frequency.json', document_frequency, True)
save_dict(DICTS + '/total_frequency.json', total_frequency, True)
