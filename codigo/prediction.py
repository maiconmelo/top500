#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 23:44:25 2021

@author: maicon
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping

# Parâmetros
train_proportion = 0.7
window = 2
neuronios = 64
camada_intermed = False
otimizador ='adam'
epocas = 50000
steps_ahead = 1
    
def create_dataset(dataset_train, dataset_test):
    
    training_set = dataset_train.values
    training_set = training_set.reshape(training_set.shape[0], 1)
    
    test_set = dataset_test.values
    test_set = test_set.reshape(test_set.shape[0], 1)
    
    # Normalização dos dados de treino
    sc = MinMaxScaler(feature_range = (0, 1))   
    training_set_scaled = sc.fit_transform(training_set)

   
    trainSize = len(training_set_scaled)
    X_train = []
    y_train = []
    for i in range(window, trainSize):
        X_train.append(training_set_scaled[i-window:i, 0])
        y_train.append(training_set_scaled[i, 0])
    
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    dataset_total = pd.concat((dataset_train.iloc[:], dataset_test.iloc[:]), axis = 0)
    testLength = len(dataset_test)
    inputs = dataset_total[len(dataset_total) - testLength - window:].values
    inputs = inputs.reshape(inputs.shape[0],1)
    
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(window, inputs.shape[0]): 
        X_test.append(inputs[i-window:i, 0])
        
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))   
    y_test = test_set

    return X_train, y_train, X_test, y_test, sc, training_set, test_set

def split_data(df_prediction):
    # Carregando do dataset
    dataset = df_prediction[df_prediction['rank'] == 1].rmax
    dataset = dataset[35:]
    dataset_index = int(len(dataset) * train_proportion)
    
    dataset_train = dataset.iloc[:dataset_index]
    dataset_test = dataset.iloc[dataset_index:]
   

    return dataset_train, dataset_test    


def train_model(X_train, y_train, X_test, y_test):
    callbacks = [
        ReduceLROnPlateau(patience=10, factor=0.5, verbose=True), # Redução da taxa de aprendizado
        ModelCheckpoint('best.model', save_best_only=True),
        EarlyStopping(patience=25, verbose=True) # Interrupção do treinamento pelo monitoramento do erro de validação
    ]

   

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
    #resp = model.fit(X_train, y_train, epochs=epocas, batch_size=12, verbose=0, callbacks=callbacks, validation_data=(X_test, y_test))
    resp = model.fit(X_train, y_train, verbose=0, epochs=epocas, batch_size=12)

    
    return model

def evaluate_model(model, X_train, X_test, y_test, training_set, test_set, sc):
    predicted_values = model.predict(X_test)
    predicted_values = sc.inverse_transform(predicted_values)
    
   
    allTargetData = np.vstack((training_set, test_set))
    #allTargetData = np.vstack((y_train, y_test))
    training_predicted_values = model.predict(X_train)
    training_predicted_values = sc.inverse_transform(training_predicted_values)
    allForecastedData = np.vstack((training_set[0:window], training_predicted_values, predicted_values))
    plt.plot(allTargetData, color = 'red', label = 'Real')
    plt.plot(allForecastedData, color = 'blue', label = 'Previsto')
    plt.title(f'Previsão de série temporal ({epocas}, {neuronios})')
    plt.xlabel('Edições do Top500')
    plt.ylabel('Desempenho Nominal')
    plt.legend()
    plt.show()
    

    rmse = math.sqrt(mean_squared_error(y_test, predicted_values))
    print('RMSE: ', rmse)

    mse = mean_squared_error(y_test, predicted_values)
    print('MSE: ',mse)

    mape = np.mean(np.abs((y_test - predicted_values) / y_test)) * 100
    print('MAPE: ',mape, '%')    

def forecast(model, dataset_test, window, steps_ahead, sc):
    last_data = dataset_test[-window:].values
    last_data = np.reshape(last_data, (1, last_data.shape[0], 1)) 
    
    for step in range(steps_ahead):
        predicted_value = model.predict(last_data)
        predicted_value = sc.inverse_transform(predicted_value)
        new_first = last_data[0][-1].copy()
        last_data[0][-1] = predicted_value.copy()
        last_data[0][0] = new_first.copy()
        
    print(f"Valor previsto: {predicted_value[0][0]} - Passos: {steps_ahead}")

def rmax(df_top500):
    df_prediction = df_top500.copy()
    
    dataset_train, dataset_test = split_data(df_prediction)
    X_train, y_train, X_test, y_test, sc, training_set, test_set = create_dataset(dataset_train, dataset_test)
    model = train_model(X_train, y_train, X_test, y_test)
    evaluate_model(model, X_train, X_test, y_test, training_set, test_set, sc)
    forecast(model, dataset_test, window, steps_ahead, sc)

   