""" DATABASE FOR MACHINE LEARNING
In this code, all columns that would provide essential information for machine
learning are retained, sorting them into necessary features and the target variable. The final column should
represent the target variable.
It is advisable to transform the intensity values (PSA) into a base 10 logarithmic
scale (log10). It has to be executed once for each intensity measure.
Example of features and target: Source ID,Site Lat,Site Lon,Magnitude,Hypocenter Lat,Hypocenter Lon,Hypocenter Depth,
EuclideanDistance,Azimuth,Intensity Value

Author: Rut Blanco (Last modification: September 2023) """

import pandas as pd
import numpy as np

dfDataSet0 = pd.read_csv("/path/to/Database.csv")

# Generate features of the model
dfFeatures = pd.DataFrame()
dfFeatures["Site Lat"] = dfDataSet0["Site Lat"]
dfFeatures["Site Lon"] = dfDataSet0["Site Lon"]
dfFeatures["Magnitude"] = dfDataSet0["Magnitude"]
dfFeatures["Hypocenter Lat"] = dfDataSet0["Hypocenter Lat"]
dfFeatures["Hypocenter Lon"] = dfDataSet0["Hypocenter Lon"]
dfFeatures["Hypocenter Depth"] = dfDataSet0["Hypocenter Depth"]
dfFeatures["EuclideanDistance"] = dfDataSet0["EuclideanDistance_EQ-Sta"]
dfFeatures["Azimuth"] = dfDataSet0["Azim_EQ-Sta"]
dfFeatures["Lower Intensity Value 10s"] = np.log10(dfDataSet0["Intensity Value"])
dfFeatures["Target Intensity Value 3s"] = np.log10(dfDataSet0["Intensity Value 3s"])

dfFeatures.to_csv("/path/to/FolderOut/ML_Database.csv", index=False)




