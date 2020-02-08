import numpy as np
import keras
from keras.layers import Input, Dense
from keras.models import Sequential, Model



input_layer = Input((4,))
hidden = Dense(4, activation="softmax")(input_layer)
hidden = Dense(96, activation="softmax")(hidden)
hidden = Dense(3, activation="sigmoid")(hidden)

model = Model(inputs=input_layer, outputs=hidden)

model.compile(loss='categorical_crossentropy', optimizer='sgd')