'''
STEP6: GENERATE FEATURES FOR THE MODEL
In this step the database is filtered with only the necessary features and target. 
It has to be executed once for each intensity measure.
'''

import pandas as pd 
from datetime import datetime
import numpy as np 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import scipy.io
from sklearn.svm import SVR  
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import *
import pickle
import getopt
import sys
import time
import joblib

#Diferent databases
df_ini = pd.read_csv("/path/Database/")

dfDataSet0 = df_ini

#Features and target: Source ID,Rupture ID,Rupture Variation ID,Site Lat,Site Lon,Magnitude,Hypocenter Lat,Hypocenter Lon,Hypocenter Depth,EuclideanDistance,Azimuth,Intensity Value

#Generate features of the model
dfFeatures = pd.DataFrame()
dfFeatures["Source ID"] =  dfDataSet0["Source ID"]
dfFeatures["Site Lat"] = dfDataSet0["Site Lat"]
dfFeatures["Site Lon"] = dfDataSet0["Site Lon"]
dfFeatures["Magnitude"] = dfDataSet0["Magnitude"]
dfFeatures["Hypocenter Lat"] = dfDataSet0["Hypocenter Lat"]
dfFeatures["Hypocenter Lon"] = dfDataSet0["Hypocenter Lon"]
dfFeatures["Hypocenter Depth"] = dfDataSet0["Hypocenter Depth"]
dfFeatures["EuclideanDistance"] = dfDataSet0["EuclideanDistance"]
dfFeatures["Azimuth"] = dfDataSet0["Azimuth"]
dfFeatures["Intensity Value"] = np.log10(dfDataSet0["PSA"])

# Export to CSV
dfFeatures.to_csv("AllData.csv", index=False)


