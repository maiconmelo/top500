#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:46:31 2021

@author: maicon
"""


import plot 
import config
import pandas as pd
import numpy as np
import country_converter as cc
import statsmodels.api as sm
import scipy.stats as stats
from statsmodels.formula.api import ols


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
    trainY = trainY / 30
    testY = testY / 30

    return trainX, testX, trainY, testY



def split_dataset(df_prediction, look_back):
    
    dataset = df_prediction[df_prediction['rank'] == 1][['list','rmax']]
    dataset = dataset.values
    dataset = dataset.astype('float32')
    
    # Tamanho da janela
  
    # Divide os dados de treino (2/3) e teste (1/3)
    # Note que a divisão não é aleatória, mas sim sequencial
    train_size = int(len(dataset) * 0.80)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size-look_back-1:len(dataset),:]
    
    return train, test

def define_ltsm():
    model = Sequential()
    model.add(LSTM(32, input_shape=(look_back, 1), return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.summary()
    
    return model


def train_model():
    callbacks = [
    ReduceLROnPlateau(patience=10, factor=0.5, verbose=True),
    ModelCheckpoint('best.model', save_best_only=True),
    EarlyStopping(patience=25, verbose=True)
    ]

    
    
    history = model.fit(trainX, trainY, epochs=5000, batch_size=24, validation_data=(testX, testY),
                    verbose=0, callbacks=callbacks)
    return history

    
def exaflop(df_top500):
    df_prediction = df_top500.copy()
    look_back = 12

    
    train, test = split_dataset(df_prediction, look_back)
    trainX, testX, trainY, testY = prepare_dataset(train, test, look_back)
    model = define_ltsm()
    history = train_model()
    
   
    
    
    
    
    
    
    
    
    
    
    
    