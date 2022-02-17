import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.model_selection import train_test_split
from keras.layers import Flatten
from keras.models import load_model
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from csv import reader
from keras.optimizers import SGD
from sklearn.preprocessing import LabelEncoder
import numpy as np
import keras.layers
from keras.models import model_from_json
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D

import random
# load dataset
# open file in read mode
#openpalm 0
#fist 1
#point 2
#twopoint 3
def save_model(model):
    # saving model
    json_model = model.to_json()
    open('model_architecture.json', 'w').write(json_model)
    # saving weights
    model.save_weights('model_weights.h5', overwrite=True)
def load_model():
    # loading model
    model = model_from_json(open('model_architecture.json').read())
    model.load_weights('model_weights.h5')
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

def preprocess(filename,classi):
    with open(filename, 'r') as read_obj:
    # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
        store = []
        for row in csv_reader:
        # row variable is a list that represents a row in csv
            current = np.array(row)
            store.append(current)


        final = store
        finaly = np.zeros(len(final))
        for x in range(0, finaly.shape[0]):
            finaly[x]=classi
        return(final,finaly)


# pureLink  (is, equals) = are, is
# possLink  (has, belongs to) > have, possess
# negLink  (inverts relation) ! n't, not
# bindLink (binds multiple var) &
# divLink (or, divides multiple variables) ^
# condLink (requires reorder, conditional) |
# tempLink (time dependent link) * feels

tempLink, tempLink_y= preprocess("memory/templink.csv",0)
pureLink, pureLink_y= preprocess("memory/purelink.csv",1)
possLink, possLink_y = preprocess("memory/posslink.csv",2)
condLink, condLink_= preprocess("memory/condlink.csv",3)

total = len(tempLink)+len(pureLink)+len(possLink)+len(condLink)

temp = np.zeros((len(tempLink), 63))
pure = np.zeros((len(pureLink), 63))
poss = np.zeros((len(possLink), 63))
cond = np.zeros((len(condLink), 63))

for x in range(0, palm.shape[0]):
    palm[x] = openpalm[x]
for x in range(0, cfist.shape[0]):
    cfist[x] = fist[x]
for x in range(0, cpoint.shape[0]):
    cpoint[x] = point[x]
for x in range(0, ctwopoint.shape[0]):
    ctwopoint[x] = twopoint[x]

xbuild = np.concatenate((palm,cfist))
xbuild1 = np.concatenate((cpoint,ctwopoint))
X = np.concatenate((xbuild,xbuild1))
ybuild = np.concatenate((opy,fy))
ybuild1 = np.concatenate((py,tpy))
ybuild = np.concatenate((ybuild,ybuild1))
Y = ybuild


X = np.delete(X, list(range(0, X.shape[1], 3)), axis=1)

X= X.reshape(X.shape[0], 21, 2)

#random.shuffle(bigboy)

#bigboy = np.asarray(bigboy)
#print((bigboy.shape))


# encode class values as integers

# fit scaler on data

encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)
'''
'''
# define baseline model
def baseline_model():
    model = Sequential()
    model.add(keras.Input(shape=(21,2)))
    model.add(Dense(164, activation='relu'))
    model.add(Dense(164, activation='relu'))
    model.add(Dense(164, activation='relu'))
    model.add(Dense(164, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(164, activation='relu'))
    model.add(Dense(164, activation='relu'))
    model.add(Dense(164, activation='relu'))
    model.add(Dense(164, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(21, activation='relu'))
    model.add(Dense(21, activation='relu'))
    model.add(Dense(21, activation='relu'))
    model.add(Dense(4, activation='softmax'))

	# Compile model

    model.compile(loss="sparse_categorical_crossentropy",  optimizer='adam', metrics=["accuracy"])
    return model

#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
#estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=10, verbose=1)
#model = baseline_model()
#model.fit(X_train, Y_train, epochs=200, batch_size=5, verbose=1)
#save_model(model)

# load

def pred_gen():
    model = load_model()
    while(True):
        val = yield
        #print("  ")
        if val is not None:
            if(len(val)==1):
                yield([np.argmax(model.predict(np.array([val[0],])), axis=-1)])
            elif len(val)==2 :
                yield([np.argmax(model.predict(np.array([val[0],val[1]])), axis=-1)])

#model = load_model()
#converter = tf.lite.TFLiteConverter.from_keras_model(model)
#tflite_model = converter.convert()
#predictions
#predictions = model.predict_classes(X_test, verbose=0)
#for x in range(0, len(predictions)):
    #print(str(int(Y_test[x]))+"=>"+str(predictions[x]))

# reverse encoding
