import pandas as pd
import seaborn as sns
import matplotlib
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import mean_absolute_error,mean_squared_error
from ast import literal_eval
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.layers import LSTM,Embedding
import numpy as np
import math

def get_matrices(dataset):
    print(dataset.head()) 
    print(dataset.dtypes)
    headlines = dataset['headlines']
    
    matrix_headlines = list()
    
    for i in headlines.keys():
      matrix_headlines.append([float(x) for x in headlines[i]])
    
    variations = dataset['variations']
    print(variations)

    matrix_variations = list()
    
    for i in variations.keys():
        matrix_variations.append([float(x) for x in variations[i]])
    

    return  (matrix_headlines,matrix_variations)

def scale_matrix(matrix):
    
    standard_scaler = preprocessing.StandardScaler()
    standard_scaler.fit(matrix)
    matrix = standard_scaler.transform(matrix)
    
    return ([list(x) for x in matrix],standard_scaler)

def get_preprocessed_dataset(dataset):
    headlines,variations = get_matrices(dataset)
    headlines,scaler = scale_matrix(headlines)
    dataset['headlines'] = headlines
    dataset['variations'] = variations
    
    return (dataset,scaler)


def create_model_dnn(input_size,output_size):
    model = Sequential()
    model.add(Dense(64,input_size))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(output_size,activation='softmax'))
    
    model.compile(optimizer='rmsprop',loss='mse',metrics=['mean_squared_error'])
    
    return model

def create_model_lstm(input_size,output_size):
    model = Sequential()
    model.add(Embedding(input_size,output_size))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(output_size,activation='sigmoid'))
    
    model.compile(loss='mse',optimizer='rmsprop',
                  metrics=['mean_squared_error'])
    
    return model

def get_model(dataset,create_model):
    preprocessed_dataset,scaler = get_preprocessed_dataset(dataset)
    X = np.array(preprocessed_dataset['headlines'].to_list())
    y = np.array(preprocessed_dataset['variations'].to_list())
    model = create_model(len(X[0]),len(y[0]))
    model.fit(X,y,batch_size=32,epochs=10)
    return (model,scaler)

def get_model_dnn(dataset):
    return get_model(dataset,create_model_dnn)

def get_model_lstm(dataset):
    return get_model(dataset,create_model_lstm)
