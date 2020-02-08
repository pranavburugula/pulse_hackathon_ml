import numpy as np
import keras
from keras.layers import Input, Dense, LSTM, TimeDistributed
from keras.models import Sequential, Model
import csv

print('Loading data')
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    data_list = []
    for row in reader:
        data_list.append(row)
    data = np.array(data_list)
    print(data.shape)

with open('test.csv', 'r') as f:
    reader = csv.reader(f)
    data_list = []
    for row in reader:
        data_list.append(row)
    test = np.array(data_list)

print('Done loading data')

print('Reshaping data')
print(data.shape)
X_train = np.zeros((data.shape[0] - 2, 2, 4))
y_train = np.zeros((data.shape[0] - 2, 2, 4))

X_test = np.zeros((test.shape[0] - 2, 2, 4))
y_test = np.zeros((test.shape[0] - 2, 2, 4))

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
model = Sequential()
model.add(LSTM(4, return_sequences=True, input_shape=(2,4)))
model.add(TimeDistributed(Dense(4, activation='sigmoid'), input_shape=(2, 4)))

model.compile(loss='mean_absolute_percentage_error', optimizer='rmsprop', metrics=['accuracy'])
print('Training')
model.fit(X_train, y_train, batch_size=32, epochs=100, validation_split=0.3, shuffle=False)

outFilepath = 'Model.json'
# serialize model to JSON
model_json = model.model.to_json()
with open(outFilepath, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
outFilepath = "Model.h5"
model.save_weights(outFilepath)
print("Saved model to disk")

print('Done training')
print(model.summary())
metrics = model.evaluate(X_test, y_test)
print(metrics[0])