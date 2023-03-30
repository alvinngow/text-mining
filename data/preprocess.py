import nltk
import re
import csv
import os
import pandas as pd
from nltk.corpus import PlaintextCorpusReader
from nltk.stem import WordNetLemmatizer

stop_list = nltk.corpus.stopwords.words('english')
lemmatizer = WordNetLemmatizer()

import gensim
# open csv, convert to txt, return corpus
# def load_corpus(dir, text_column):
#     for file in os.listdir(dir):
#         if file.endswith(".csv"):
#             csv_path = os.path.join(dir, file)
#             txt_path = os.path.splitext(csv_path)[0] + ".txt"  # use same name as CSV file but with .txt extension
#             with open(txt_path, "w") as output:
#                 df = pd.read_csv(csv_path)
#                 for sentence in df[text_column]:
#                     output.write(str(sentence) + "\n") 
#     corpus = PlaintextCorpusReader(dir, '.+\.txt',)

#     return corpus

# open csv, convert to txt, return corpus

def load_corpus(dir):
    # dir is a directory with plain text files to load.
    corpus = nltk.corpus.PlaintextCorpusReader(dir, '.+\.txt')
    return corpus

def corpus2docs(corpus):
    # corpus is a object returned by load_corpus that represents a corpus.
    fids = corpus.fileids()
    docs1 = []
    for fid in fids:
        doc_raw = corpus.raw(fid)
        doc = nltk.word_tokenize(doc_raw)
        docs1.append(doc)
    docs2 = [[w.lower() for w in doc] for doc in docs1]
    docs3 = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs2]
    docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]
    docs5 = [[lemmatizer.lemmatize(w) for w in doc] for doc in docs4]
    return docs5

def docs2vecs(docs, dictionary):
    # docs is a list of documents returned by corpus2docs.
    # dictionary is a gensim.corpora.Dictionary object.
    vecs1 = [dictionary.doc2bow(doc) for doc in docs]
    tfidf = gensim.models.TfidfModel(vecs1)
    vecs2 = [tfidf[vec] for vec in vecs1]
    return vecs2
    