#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 23:44:25 2021

@author: maicon
"""

# %tensorflow_version 1.x
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping

import math
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler



def rmax(df_top500):
    df_prediction = df_top500.copy()
    
    train_proportion = 0.86
    
    dataset = df_prediction[df_prediction['rank'] == 1].rmax
    dataset_index = int(len(dataset) * train_proportion)
    
    dataset_train = dataset.iloc[:dataset_index]
    training_set = dataset_train.values
    training_set = training_set.reshape(training_set.shape[0], 1)

    dataset_test = dataset.iloc[dataset_index:]
    test_set = dataset_test.values
    test_set = test_set.reshape(test_set.shape[0], 1)


    """### gráfico da série temporal"""
    '''
    plt.plot(training_set)
    plt.xlabel("tempo")
    plt.ylabel("Número de passageiros x10^3")
    plt.title("Passageiros de avião")
    plt.show()
    '''
    
    sc = MinMaxScaler(feature_range = (0, 1))   
    training_set_scaled = sc.fit_transform(training_set)

    window = 4
    trainSize = len(training_set_scaled)
    X_train = []
    y_train = []
    for i in range(window, trainSize):
        X_train.append(training_set_scaled[i-window:i, 0])
        y_train.append(training_set_scaled[i, 0])
    
    X_train, y_train = np.array(X_train), np.array(y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    callbacks = [
        ReduceLROnPlateau(patience=10, factor=0.5, verbose=True), # Redução da taxa de aprendizado
        ModelCheckpoint('best.model', save_best_only=True),
        EarlyStopping(patience=25, verbose=True) # Interrupção do treinamento pelo monitoramento do erro de validação
    ]

    neuronios = 80
    camada_intermed = False
    otimizador ='adam'
    epocas = 800

    model = Sequential()

    # Camada de entrada com o janelamento e identificação se será feito em duas camadas
    model.add(LSTM(neuronios, input_shape=(window, 1), return_sequences=camada_intermed))
    model.add(Dropout(0.2))

    # Camada intermediária
    if camada_intermed:
        model.add(LSTM(neuronios, return_sequences=False))
        model.add(Dropout(0.2))

    # Camada de saída
    model.add(Dense(1))

    # Definição de métrica de erro e otimizador
    model.compile(loss='mean_squared_error', optimizer=otimizador)

    # Processa o modelo
    #resp = model.fit(X_train, y_train, epochs=epocas, batch_size=24, verbose=0, callbacks=callbacks)
    resp = model.fit(X_train, y_train, verbose=0, epochs=epocas, batch_size=12)


    #dataset_test = pd.read_csv('data/rmax_test.csv')
    #test_airline = dataset_test.values

    dataset_total = pd.concat((dataset_train.iloc[:], dataset_test.iloc[:]), axis = 0)
#    dataset_total = pd.concat((training_set, test_set), axis = 0)
    testLength = len(dataset_test)
    inputs = dataset_total[len(dataset_total) - testLength - window:].values
    inputs = inputs.reshape(inputs.shape[0],1)
    
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(window, inputs.shape[0]): 
        X_test.append(inputs[i-window:i, 0])
        
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_airline = model.predict(X_test)
    predicted_airline = sc.inverse_transform(predicted_airline)


    allTargetData = np.vstack((training_set, test_set))
    training_predicted_airline = model.predict(X_train)
    training_predicted_airline = sc.inverse_transform(training_predicted_airline)
    allForecastedData = np.vstack((training_set[0:window], training_predicted_airline, predicted_airline))
    plt.plot(allTargetData, color = 'red', label = 'Real')
    plt.plot(allForecastedData, color = 'blue', label = 'Previsto')
    plt.title('Previsão de série temporal')
    plt.xlabel('Tempo')
    plt.ylabel('Passageiros')
    plt.legend()
    plt.savefig('predictions_training_test.svg')
    plt.show()


    rmse = math.sqrt(mean_squared_error(test_set, predicted_airline))
    print('RMSE: ', rmse)

    mse = mean_squared_error(test_set, predicted_airline)
    print('MSE: ',mse)

    mape = np.mean(np.abs((test_set - predicted_airline) / test_set)) * 100
    print('MAPE: ',mape, '%')    