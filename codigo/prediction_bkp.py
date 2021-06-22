#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:46:31 2021

@author: maicon
"""


import matplotlib.pyplot as plt
import config
import math
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Conv1D, Dropout
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

np.random.seed(7)

# Recebe uma série e converte em uma matriz com séries deslocadas.
def create_dataset(dataset, look_back, std):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back), 0]-dataset[i, 0]
        a /= std
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0]-dataset[i + look_back-1, 0])
    return np.array(dataX), np.array(dataY)


def prepare_dataset(train, test, look_back):
    std = train[:, 0].std()
    trainX, trainY = create_dataset(train, look_back, std)
    testX, testY = create_dataset(test, look_back, std)


    trainX = trainX.reshape(-1, look_back, 1)
    testX = testX.reshape(-1, look_back, 1)
    #trainY = trainY / 30
    #testY = testY / 30

    return trainX, testX, trainY, testY

def define_dataset(df_prediction):
    dataset = df_prediction[df_prediction['rank'] == 1][['rmax']]
    dataset = dataset.values
    dataset = dataset.astype('float32')
    
    return dataset


def split_dataset(dataset, look_back):
    train_size = int(len(dataset) * 0.80)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size-look_back-1:len(dataset),:]
    
    return train, test

def define_ltsm(look_back):
    model = Sequential()
    model.add(LSTM(16, input_shape=(look_back, 1), return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.summary()
    
    return model


def train_model(model, trainX, trainY, testX, testY):
    callbacks = [ReduceLROnPlateau(patience=10, factor=0.5, verbose=True),
                 ModelCheckpoint('best.model', save_best_only=True),
                 EarlyStopping(patience=25, verbose=True)
    ]

    history = model.fit(trainX, trainY, epochs=50, batch_size=24, 
                        validation_data=(testX, testY),verbose=0, 
                        callbacks=callbacks
    )
    
    return history

def evaluate_model(history, model, trainX, trainY, testX, testY, dataset, look_back):
    df_history = pd.DataFrame(history.history)
    ax = df_history[['val_loss', 'loss']].plot(figsize=(10, 5))
    df_history['lr'].plot(ax=ax.twinx(), color='gray')
    
    # Realiza as previsões. Notar que a utilidade de prever trainX é nenhuma. Serve apenas para exibir no gráfico.

    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    # Calcula os erros de previsão
    trainScore = math.sqrt(mean_squared_error(trainY, trainPredict[:,0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(testY, testPredict[:,0]))
    print('Test Score: %.2f RMSE' % (testScore))


    # shift train predictions for plotting
    trainPredictPlot = (trainPredict * 2) + dataset[look_back:len(trainPredict)+look_back, 0]

    # shift test predictions for plotting
    testPredictPlot = (testPredict * 2) + dataset[len(trainPredict)+(look_back)-1:len(dataset), 0]

    # plot baseline and predictions
    plt.figure(figsize=(20, 10))
    plt.plot(dataset)
    plt.plot(look_back+np.arange(len(trainPredictPlot)), trainPredictPlot)
    plt.plot(look_back+np.arange(len(testPredictPlot))+len(trainPredictPlot)-1, testPredictPlot)
    plt.show()

    
def exaflop(df_top500):
    df_prediction = df_top500.copy()
    look_back = 12

    dataset = define_dataset(df_prediction)
    train, test = split_dataset(dataset, look_back)
    trainX, testX, trainY, testY = prepare_dataset(train, test, look_back)
    model = define_ltsm(look_back)
    history = train_model(model, trainX, trainY, testX, testY)
    evaluate_model(history, model, trainX, trainY, testX, testY, dataset, look_back)
   
    
    
    
    
    
    
    
    
    
    
    
    