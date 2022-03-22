#!/usr/bin/env python

import spacy
import os
import sys
from nltk.stem import PorterStemmer
porter=PorterStemmer()

from util.preprocessing import addCharInformation, createMatrices, addCasingInformation
from neuralnets.BiLSTM import BiLSTM
from classes import class_dict


def preprocess(text: str, spacy_fx, lstm_model):
    sentences = []
    doc = spacy_fx(text)
    for sent in doc.sents:
        sentences.append({'tokens': [token.text for token in list(sent)],
                          'token_spans': [(token.idx, len(token)+token.idx) for token in sent]})

    addCharInformation(sentences)  # TODO: get rid of in-place mutation
    addCasingInformation(sentences)  # TODO: get rid of in-place mutation
    data_matrix = createMatrices(sentences, lstm_model.mappings, True)

    return data_matrix, sentences


def search_classes(text):
    for key, value in class_dict.items():
        if [c for c in value if c == text]:
            return key
    else: return 'NIL'


def format_output(tags, sentences):
    events = []
    for sentenceIdx in range(len(sentences)):
        tokens = sentences[sentenceIdx]['tokens']
        spans = sentences[sentenceIdx]['token_spans']

        for tokenIdx in range(len(tokens)):
            tokenTags = []
            for modelName in sorted(tags.keys()):
                tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])

            event_dict = {}
            event_dict['offset_start'] = spans[tokenIdx][0]
            event_dict['offset_end'] = spans[tokenIdx][1]
            event_dict['model_output'] = "\t".join(tokenTags)
            event_dict['text'] = porter.stem((tokens[tokenIdx]).lower())
            event_dict['tag'] = search_classes(event_dict['text'])
            events.append(event_dict)

    return events


def detect_events(text: str, spacy_fx, lstm_model):
    data_matrix, sentences = preprocess(text, spacy_fx, lstm_model)
    tags = lstm_model.tagSentences(data_matrix)  # predict tags
    return format_output(tags, sentences)
