from __future__ import print_function
from sentence_types import encode_data, import_embedding, encode_phrases
import os
import sys

import numpy as np
import keras

from sentence_types import load_encoded_data
from sentence_types import encode_data, import_embedding
from sentence_types import get_custom_test_comments

from keras.preprocessing import sequence
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D

from keras.preprocessing.text import Tokenizer

def load_model():
    model_name      = "Language/STClassifier/models/cnn"
    embedding_name  = "Language/STClassifier/data/default"
    json_file = open(model_name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)

    # load weights into new model
    model.load_weights(model_name + ".h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return(model)


def encode_predict(test_comments, data_split=1.0, embedding_name="Language/STClassifier/data/default", add_pos_tags_flag=False):
    # Import prior mapping
    word_encoding = None
    if embedding_name:
        word_encoding, category_encoding = import_embedding(embedding_name)
    # Encode comments word + punc, using prior mapping or make new
    encoded_comments, word_encoding, \
        word_decoding = encode_phrases(test_comments, word_encoding,
                                   add_pos_tags_flag=add_pos_tags_flag)
    q = sequence.pad_sequences(encoded_comments, maxlen = 500)
    return q

def run(text, modelin):
    model = modelin
    q = encode_predict([text], data_split=1.0, embedding_name="Language/STClassifier/data/default", add_pos_tags_flag=True)
    predictions = model.predict(q)
    predictions = predictions.argmax(axis=1)
    return(predictions)
#null, question, statement, command


def STClassGen():
    model = load_model()
    yield(True)
    while(True):
        val = yield
        if(val is not None):
            pred = run(val, model)
            yield(pred)
        else:
            pass
