from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import pickle
import nltk
import validators
import demoji
import string
import re
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag

from sklearn.metrics.pairwise import cosine_similarity

def display_topics(model, feature_names, no_top_words):
    topic_dict = {}

    for topic_idx, topic in enumerate(model.components_):
        topic_dict[f"Topic {topic_idx}"] = " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])

    return topic_dict

def ProcessInput(inputArray):
    document = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    for text in inputArray:
        sentence = ""
        tokenized_text = nltk.word_tokenize(text)
        pos_tags = pos_tag(tokenized_text)
        tonkenized_text = [token for token, pos in pos_tags if pos not in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'VB']]
        for token in tokenized_text:
            if token not in stop_words and not validators.url(token) and token not in string.punctuation and not re.search(r'(chat[-\s])?gpt|\d+', token.lower()):
                sentence += lemmatizer.lemmatize(token) + ' '
        sentence = demoji.replace(string = sentence, repl = "")
        document.append(sentence[:-1])
    return document

def ShowDocInTopic(topic, count, model_output, model,document_train):
    lda_df = pd.DataFrame({"text": document_train, "topic": model_output.argmax(axis=1)})
    pd.set_option('display.max_colwidth', None)
    return lda_df[lda_df['topic'] == topic].head(count)

class LDAView(APIView):
    def get(self, request, *args, **kwargs):

        untuned = None
        vectorizer = None
        best_lda = None
        document_train= None
        train_vect = None
        best_lda_output = None
        untuned_output = None
        with open('untuned.bin','rb') as u:
            untuned = pickle.load(u)
        with open('vectorizer.pk','rb') as v:
            vectorizer = pickle.load(v)
        with open('best_lda.pk','rb') as v:
            best_lda = pickle.load(v)
        with open('document_train.pk','rb') as v:
            document_train = pickle.load(v)
        with open('best_lda_output.pk','rb') as v:
            best_lda_output = pickle.load(v)
        with open('train_vect.pk','rb') as v:
            train_vect = pickle.load(v)
        with open('untuned_output.pk','rb') as v:
            untuned_output = pickle.load(v)

        feature_names = vectorizer.get_feature_names_out()
        untuned_topics = display_topics(untuned, feature_names, 15)
        best_lda_topics = display_topics(best_lda, feature_names, 15)
        
        sentence = request.GET.get("sentence")
        new_doc = vectorizer.transform(ProcessInput([sentence]))
        untuned_topic_probs = untuned.transform(new_doc)
        best_topic_probs = best_lda.transform(new_doc)
        best_topic = best_topic_probs.argmax()
        untuned_topic = untuned_topic_probs.argmax()

        doc_topic = ShowDocInTopic(best_topic_probs.argmax(), 50, best_lda_output, best_lda,train_vect)
        similarity_scores = []
        for i, doc in doc_topic.iterrows():
            sim_score = cosine_similarity(new_doc, train_vect[i])[0][0]
            similarity_scores.append((i, sim_score))

        sorted_docs = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        top_10_docs = sorted_docs[:5]
        pred_topic_docs = []
        for doc_id, sim_score in top_10_docs:
            pred_topic_docs.append(document_train[doc_id])

        doc_topic = ShowDocInTopic(untuned_topic_probs.argmax(), 50, untuned_output, untuned,train_vect)
        similarity_scores = []
        for i, doc in doc_topic.iterrows():
            sim_score = cosine_similarity(new_doc, train_vect[i])[0][0]
            similarity_scores.append((i, sim_score))

        sorted_docs = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        top_10_docs = sorted_docs[:5]
        untuned_topic_docs = []
        for doc_id, sim_score in top_10_docs:
            untuned_topic_docs.append(document_train[doc_id])

        res = {
            "untuned_topics":untuned_topics,
            "best_lda_topics":best_lda_topics,
            'untuned_prob' : untuned_topic,
            'untuned_example':untuned_topic_docs,
            'best_prob':best_topic,
            'best_lda_example':pred_topic_docs
        }
        print(res)
        return Response(res, status=status.HTTP_200_OK)

class SAView(APIView):
    
    def get(self, request, *args, **kwargs):
        sentence = request.GET.get("sentence")
        log = None
        svc = None
        vectorizer = None

        with open('log_pred.pk','rb') as f:
            log = pickle.load(f)
        with open('svc.pk','rb') as f:
            svc = pickle.load(f)
        with open('sa_vect.pk','rb') as f:
            vectorizer = pickle.load(f)
        X_pred_vect = vectorizer.transform([sentence])
        
        ylog_pred = log.predict(X_pred_vect)
        ysvc_pred = svc.predict(X_pred_vect)

        res = {
            'log_pred':ylog_pred,
            'svc_pred':ysvc_pred
        }
        
        return Response(res, status=status.HTTP_200_OK)

