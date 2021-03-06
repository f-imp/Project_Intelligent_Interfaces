import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras import Sequential
from keras.layers import Dense, Dropout, Flatten, LSTM, Conv1D, MaxPooling1D
from keras.optimizers import Adam


def model_1(shape, no_output, learning_rate, lf, af):
    name = "LSTM_with_return_sequences"
    model = Sequential()
    model.add(LSTM(256, return_sequences=True, input_shape=shape))
    model.add(LSTM(512))
    model.add(Dense(1024))
    model.add(Dropout(0.2))
    model.add(Dense(1024))
    model.add(Dense(1024))
    model.add(Dense(no_output, activation='sigmoid'))
    model.compile(optimizer=Adam(lr=learning_rate),
                  loss=[lf],
                  metrics=[af])
    return model, name


def model_2(shape, no_output, learning_rate, lf, af):
    name = "Convolutional_Network"
    model = Sequential()
    model.add(Conv1D(filters=256, kernel_size=5, padding='causal', input_shape=shape))
    model.add(Conv1D(filters=512, kernel_size=3, padding='causal'))
    model.add(Conv1D(filters=1024, kernel_size=3, padding='causal'))
    model.add(Conv1D(filters=64, kernel_size=3, padding='causal'))
    model.add(MaxPooling1D(pool_size=3))
    model.add(Flatten())
    model.add(Dense(no_output, activation='sigmoid'))
    model.compile(optimizer=Adam(lr=learning_rate),
                  loss=[lf],
                  metrics=[af])
    return model, name


def model_3(shape, no_output, learning_rate, lf, af):
    name = "LSTM"
    model = Sequential()
    model.add(LSTM(200, input_shape=shape))
    model.add(Dense(no_output, activation='sigmoid'))
    model.compile(optimizer=Adam(lr=learning_rate),
                  loss=[lf],
                  metrics=[af])
    return model, name

def model_4(shape, no_output, learning_rate, lf, af):
    name = "LSTM_with_return_sequences2"
    model = Sequential()
    model.add(LSTM(2048, return_sequences=True, input_shape=shape))
    model.add(LSTM(1024))
    model.add(Dense(256))
    model.add(Dropout(0.7))
    model.add(Dense(128))
    model.add(Dropout(0.5))
    model.add(Dense(32))
    model.add(Dense(no_output, activation='sigmoid'))
    model.compile(optimizer=Adam(lr=learning_rate),
                  loss=[lf],
                  metrics=[af])
    return model, name

def model_5(shape, no_output, learning_rate, lf, af):
    name = "LSTM_with_return_sequences3"
    model = Sequential()
    model.add(LSTM(2048, return_sequences=True, input_shape=shape))
    model.add(LSTM(1024))
    model.add(Dense(32))
    model.add(Dropout(0.7))
    model.add(Dense(no_output, activation='sigmoid'))
    model.compile(optimizer=Adam(lr=learning_rate),
                  loss=[lf],
                  metrics=[af])
    return model, name

def model_6(shape, no_output, learning_rate, lf, af):
    name = "LSTM_with_return_sequences4"
    model = Sequential()
    model.add(LSTM(3000, return_sequences=True, input_shape=shape))
    model.add(LSTM(512))
    model.add(Dropout(0.5))
    model.add(Dense(32))
    model.add(Dense(no_output, activation='sigmoid'))
    model.compile(optimizer=Adam(lr=learning_rate),
                  loss=[lf],
                  metrics=[af])
    return model, name