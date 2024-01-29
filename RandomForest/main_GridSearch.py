"""GRID SEARCH: FIND HYPERPARAMETERS
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


from sklearn import datasets
import pandas as pd
import dislib as ds
import numpy as np
from dislib.regression import RandomForestRegressor
from _search import GridSearchCV
from sklearn.datasets import make_regression
#from dislib.preprocessing import MinMaxScaler
from dislib.utils import train_test_split
from dislib.data import load_txt_file
from pycompss.api.api import compss_wait_on, compss_barrier
from minmax_scaler import MinMaxScaler

def demostracion_grid_search():
    df = load_txt_file("/path/to/Train.csv",discard_first_row=True, col_of_index=True,block_size=(133334, 9))
    dfAll = load_txt_file("/path/to/AllDatabase.csv",discard_first_row=True, col_of_index=True,block_size=(133334, 9))
    Data_X_arr_All = dfAll[:, 0:8] #depending on the number of features
    Data_Y_arr_All = dfAll[:, 8:9] #position of the target column
    Data_X_arr = df[:, 0:8]
    Data_Y_arr = df[:, 8:9]
    scaler_X = MinMaxScaler(feature_range=(0, 1))
    scaler_X.fit(Data_X_arr_All)
    scaler_y = MinMaxScaler(feature_range=(0, 1))
    scaler_y.fit(Data_Y_arr_All)
    x_ds_train, x_ds_test, y_ds_train, y_ds_test = train_test_split(Data_X_arr, Data_Y_arr)
    x_ds_test = x_ds_test.rechunk((100000, 8))
    y_ds_test = y_ds_test.rechunk((100000, 1))#Hago el rechunk porque el train_test_split devuelve el test con un block size de 33334 en filas
    x_train = scaler_X.transform(x_ds_train)
    x_test = scaler_X.transform(x_ds_test)
    y_train = scaler_y.transform(y_ds_train)
    y_test = scaler_y.transform(y_ds_test)
    parameters = {'max_depth':(30,35,40)}  #Modify the parameters 3 by 3, with values from 10 to 50.

    rf = RandomForestRegressor(n_estimators=20, try_features='third')
    searcher = GridSearchCV(rf, parameters, cv=5)
    np.random.seed(0)
    searcher.fit(x_train, y_train)
    print("T5_RndmSplit")
    print(searcher.cv_results_['params'])
    print(searcher.cv_results_['mean_test_score'])
    pd_df = pd.DataFrame.from_dict(searcher.cv_results_)
    print(pd_df[['params', 'mean_test_score']])
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None):
        print(pd_df)
    print('best_estimator')
    print(searcher.best_estimator_)
    print(searcher.best_score_)
    print(searcher.best_params_)
    print(searcher.best_index_)
    print(searcher.scorer_)
    print(searcher.n_splits_)


if __name__ == "__main__":
    demostracion_grid_search()
