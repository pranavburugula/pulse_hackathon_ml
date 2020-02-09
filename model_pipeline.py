import numpy as np
import keras
from keras.layers import Input, Dense, LSTM, TimeDistributed
from keras.models import Sequential, Model, model_from_json
import csv

print('Loading data')
with open('train2.csv', 'r') as f:
    reader = csv.reader(f)
    data_list = []
    for row in reader:
        data_list.append(row)
    data = np.array(data_list)
    print(data.shape)

with open('test2.csv', 'r') as f:
    reader = csv.reader(f)
    data_list = []
    for row in reader:
        data_list.append(row)
    test = np.array(data_list)

print('Done loading data')

print('Reshaping data')
print(data.shape)
X_train = np.zeros((data.shape[0] - 2, 2, 2))
y_train = np.zeros((data.shape[0] - 2, 2, 2))

X_test = np.zeros((test.shape[0] - 2, 2, 2))
y_test = np.zeros((test.shape[0] - 2, 2, 2))

for i in range(data.shape[0] - 2):
    X_train[i,0] = data[i]
    X_train[i,1] = data[i+1]
    y_train[i,0] = data[i+1]
    y_train[i,1] = data[i+2]

for i in range(test.shape[0] - 2):
    X_test[i,0] = test[i]
    X_test[i,1] = test[i+1]
    y_test[i,0] = test[i+1]
    y_test[i,1] = test[i+2]

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)
print('Done reshaping data')

training = True
if(training):
    model = Sequential()
    model.add(LSTM(2, return_sequences=True, input_shape=(2,2)))
    model.add(TimeDistributed(Dense(2, activation='sigmoid'), input_shape=(2,2)))

    model.compile(loss='mean_absolute_percentage_error', optimizer='rmsprop', metrics=['accuracy'])
    print('Training')
    model.fit(X_train, y_train, batch_size=32, epochs=10, validation_split=0.3, shuffle=False)

    outFilepath = 'Model2.json'
    # serialize model to JSON
    model_json = model.model.to_json()
    with open(outFilepath, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    outFilepath = "Model2.h5"
    model.save_weights(outFilepath)
    print("Saved model to disk")

    print('Done training')
    print(model.summary())

json_file = open('Model2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights('Model2.h5')
loaded_model.compile(loss='mean_absolute_percentage_error', optimizer='rmsprop', metrics=['accuracy'])
metrics = loaded_model.evaluate(X_test, y_test)
print(metrics[0])