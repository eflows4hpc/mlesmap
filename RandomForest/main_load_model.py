""" LOAD MODEL: VALIDATION


Copyright (c) . All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY 
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from dislib.trees import RandomForestRegressor
import dislib as ds
import numpy as np
from pycompss.api.api import compss_barrier, compss_wait_on
#from sklearn.preprocessing import MinMaxScaler
#from dislib.preprocessing import MinMaxScaler
from minmax_scaler import MinMaxScaler
from dislib.model_selection import KFold
import pickle
from sklearn.metrics import *
from dislib.data.array import *
from dislib.utils import train_test_split
from dislib.data import load_txt_file
import time
import pandas as pd

def _determination_coefficient(y_true, y_pred):
    u = np.sum(np.square(y_true - y_pred))
    v = np.sum(np.square(y_true - np.mean(y_true)))
    return 1 - u / v

def make_load_model():
    ini_time = time.time()
    df = load_txt_file("/path/to/Test.csv",discard_first_row=True, col_of_index=True,block_size=(133334, 9))
    dfAll = load_txt_file("/path/to/AllDatabase.csv",discard_first_row=True, col_of_index=True,block_size=(133334, 9)) 
    Data_X_arr_All = dfAll[:, 0:8]
    Data_Y_arr_All = dfAll[:, 8:9]
    Data_X_arr = df[:, 0:8]
    Data_Y_arr = df[:, 8:9]
    scaler_X = MinMaxScaler(feature_range=(0, 1))
    scaler_X.fit(Data_X_arr_All)
    scaler_y = MinMaxScaler(feature_range=(0, 1))
    scaler_y.fit(Data_Y_arr_All)
    x_ds_test = Data_X_arr.rechunk((10000,8)) #  ((100000, 8))
    y_ds_test = Data_Y_arr.rechunk((10000,1)) #((100000, 1))#Hago el rechunk porque el train_test_split devuelve el test con un block size de 33334 en filas
    x_test = scaler_X.transform(x_ds_test)
    y_test = scaler_y.transform(y_ds_test)
    load_time = time.time()
    print("Load time", load_time - ini_time)
    print("Fitting...")
    start_time = time.time()
    rf = RandomForestRegressor(max_depth=30,n_estimators=30,try_features='third',random_state=0)
    rf.load_model("Model_T-s_RF_depth--_n_estim--_log10_-Features_----Split.save", load_format="pickle")    
    y_pred = scaler_y.inverse_transform(rf.predict(x_test))
    y_true = scaler_y.inverse_transform(y_test)
    y_pred = y_pred.collect()
    y_true = y_true.collect()
    score2 = _determination_coefficient(y_true, y_pred)
    fit_time = time.time()
    print("Fit time:", fit_time - start_time)
    score1 = rf.score(x_test, y_test, collect=True)
    score1_time = time.time()
    print("score1 time:", score1_time - fit_time)
    print("score1", score1)
    pred_time = time.time()
    print("Prediction time:", pred_time - score1_time)
    print("Total time:", pred_time - start_time)
    score2 = _determination_coefficient(y_true, y_pred)
    print("score2", score2)
    np.savetxt('y_pred_dislib_T-s_depth---_n_estimators----_val_---_Dataset_log10_-Feat_---Split.dat',y_pred)
    np.savetxt('y_true_dislib_T-s_depth---_n_estimators----_val_---_Dataset_log10_-Feat_---Split.dat',y_true) 
    mse = mean_squared_error(y_true, y_pred)
    print("mse=",mse) 
    evs = explained_variance_score(y_true,y_pred)
    print("evs=",evs)
    mae = mean_absolute_error(y_true,y_pred)
    print("mae=", mae)
    mape = 100*(abs(y_pred-y_true)/y_true)
    print("mape=", 100-np.mean(mape))
    print("coefPearson=", np.corrcoef(y_true,y_pred))
    

if __name__ == '__main__':
    make_load_model()
