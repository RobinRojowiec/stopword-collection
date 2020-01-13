"""

IDE: PyCharm
Project: corpus-analysis
Author: Robin
Filename: generate_docs
Date: 12.01.2020

"""
import pandas as pd
from tqdm import tqdm

root_folder = 'data/leipzig-corpora/'
filename: str = root_folder + 'deu_wikipedia_2016_10K-sentences.txt'
doc_folder = root_folder + 'docs'

dataframe = pd.read_csv(filename, sep='\t', header=None, names=["id", "text"])


def create_doc(filename: str, text: str):
    with open(filename, 'w+', encoding='utf-8') as txt_file:
        txt_file.write(text)


for index, row in tqdm(dataframe.iterrows(), total=len(dataframe)):
    id, text = row[0], row[1]
    create_doc(doc_folder + '/%i.txt' % id, text)
