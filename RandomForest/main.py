from dislib.trees import RandomForestRegressor
import dislib as ds
import numpy as np
from pycompss.api.api import compss_barrier, compss_wait_on
from dislib.model_selection import KFold
import pickle
from sklearn.metrics import *
from dislib.data.array import *
from dislib.utils import train_test_split
from dislib.data import load_txt_file
import time
import pandas as pd
from dislib.preprocessing import MinMaxScaler

def _determination_coefficient(y_true, y_pred):
    u = np.sum(np.square(y_true - y_pred))
    v = np.sum(np.square(y_true - np.mean(y_true)))
    return 1 - u / v

def make_regression_rf():
    ini_time = time.time()
    df = load_txt_file("/gpfs/scratch/bsc21/bsc21395/Dislib/Iceland/Dislib_IcelandRndmSplit_9Feat_3s_Train.csv",discard_first_row=True, col_of_index=True,block_size=(133334, 9))
    dfAll = load_txt_file("/gpfs/scratch/bsc21/bsc21395/Dislib/Iceland/Dislib_IcelandAllData_9Feat_3s.csv",discard_first_row=True, col_of_index=True,block_size=(133334, 9))
    Data_X_arr = df[:, 0:8]
    Data_Y_arr = df[:, 8:9]
    Data_X_arr_All = dfAll[:, 0:8]
    Data_Y_arr_All = dfAll[:, 8:9]
    x_ds_train, x_ds_test, y_ds_train, y_ds_test = train_test_split(Data_X_arr, Data_Y_arr)
    x_ds_test = x_ds_test.rechunk((100000, 8))
    y_ds_test = y_ds_test.rechunk((100000, 1))#Hago el rechunk porque el train_test_split devuelve el test con un block size de 33334 en filas
    scaler_X = MinMaxScaler(feature_range=(0, 1))
    scaler_X.fit(Data_X_arr_All)
    scaler_y = MinMaxScaler(feature_range=(0, 1))
    scaler_y.fit(Data_Y_arr_All)
    x_test = scaler_X.transform(x_ds_test)
    y_test = scaler_y.transform(y_ds_test)
    x_train = scaler_X.transform(x_ds_train)
    y_train = scaler_y.transform(y_ds_train)
    scaler_X.save_model('scaler_X_3s_Iceland_RndmSplit')
    scaler_y.save_model('scaler_Y_3s_Iceland_RndmSplit')
    load_time = time.time()
    print("Load time", load_time - ini_time)
    print("Rndm 3s n30 depth30")
    print("Fitting...")
    start_time = time.time()
    rf = RandomForestRegressor(max_depth=30,n_estimators=30,try_features='third',random_state=0)
    rf.fit(x_train, y_train)
    rf.save_model("Iceland_model_T3s_RF_depth30_n_estim30_log10_9Features_RndmSplit.save", save_format="pickle")
    fit_time = time.time()
    print("Fit time:", fit_time - start_time)
    score1 = rf.score(x_test, y_test, collect=True)
    score1_time = time.time()
    print("score1 time:", score1_time - fit_time)
    print("score1", score1)
    pred_time = time.time()
    print("Prediction time:", pred_time - score1_time)
    print("Total time:", pred_time - start_time)
    y_pred = scaler_y.inverse_transform(rf.predict(x_test))
    y_true = scaler_y.inverse_transform(y_test)
    y_true = y_true.collect()
    y_pred = y_pred.collect()
    score2 = _determination_coefficient(y_true, y_pred)
    print("score2", score2)
    np.savetxt('y_pred_dislib_T3s_depth-30_n_estimators-30_Iceland_Dataset_log10_9Feat_RndmSplit.dat',y_pred)
    np.savetxt('y_true_dislib_T3s_depth-30_n_estimators-30_Iceland_Dataset_log10_9Feat_RndmSplit.dat',y_true) 
    mse = mean_squared_error(y_true, y_pred)
    print("mse=",mse) 
    r2 = r2_score(y_true,y_pred)
    print("r2_score=",r2)
    evs = explained_variance_score(y_true,y_pred)
    print("evs=",evs)
    mae = mean_absolute_error(y_true,y_pred)
    print("mae=", mae)
    mape = 100*(abs(y_pred-y_true)/y_true)
    print("mape=", 100-np.mean(mape))
    print("coefPearson=", np.corrcoef(y_true,y_pred))

if __name__ == '__main__':
    make_regression_rf()

