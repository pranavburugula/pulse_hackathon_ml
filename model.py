import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM

class LSTMModel(object):
    def __init__(self, json, weights):
        json_file = open(json, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(weights)
        loaded_model.compile(loss='mean_absolute_percentage_error', optimizer='rmsprop', metrics=['accuracy'])
        self.model = loaded_model
    
    def get_prediction(self, sequence):
        prediction = self.model.predict_on_batch(sequence)
        return prediction
    pass