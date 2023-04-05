from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
import pandas as pd
import numpy as np
import pickle
import nltk
import validators
import demoji
import string
import re

from django.conf import settings
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag


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
class LDAView(APIView):
    def get(self, request, *args, **kwargs):

        untuned = None
        vectorizer = None
        best_lda = None
        with open('untuned.bin','rb') as u:
            untuned = pickle.load(u)
        with open('vectorizer.pk','rb') as v:
            vectorizer = pickle.load(v)
        with open('best_lda.pk','rb') as v:
            best_lda = pickle.load(v)

        feature_names = vectorizer.get_feature_names_out()
        untuned_topics = display_topics(untuned, feature_names, 15)
        best_lda_topics = display_topics(best_lda, feature_names, 15)
        
        sentence = request.GET.get("sentence")
        new_doc = vectorizer.transform(ProcessInput([sentence]))
        untuned_topic_probs = untuned.transform(new_doc)
        best_topic_probs = best_lda.transform(new_doc)
        best_topic = best_topic_probs.argmax()
        untuned_topic = untuned_topic_probs.argmax()


        res = {
            "untuned_topics":untuned_topics,
            "best_lda_topics":best_lda_topics,
            'untuned_prob' : untuned_topic,
            'best_prob':best_topic,
        }
        print(res)
        return Response(res, status=status.HTTP_200_OK)

class SAView(APIView):
        def get(self, request, *args, **kwargs):
            print("asouidh")
            sentence = request.GET.get("sentence")
            log = None
            svc = None

            with open('log_pred.pk','rb') as f:
                log = pickle.load(f)
            with open('svc.pk','rb') as f:
                svc = pickle.load(f)

            
            return Response('ok', status=status.HTTP_200_OK)

