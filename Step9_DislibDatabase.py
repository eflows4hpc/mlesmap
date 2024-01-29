""" DATABASE FOR MACHINE LEARNING
In this code, all columns that would provide essential information for machine
learning are retained, sorting them into necessary features and the target variable. The final column should
represent the target variable.
It is advisable to transform the intensity values (PSA) into a base 10 logarithmic
scale (log10). It has to be executed once for each intensity measure.
Example of features and target: Source ID,Site Lat,Site Lon,Magnitude,Hypocenter Lat,Hypocenter Lon,Hypocenter Depth,
EuclideanDistance,Azimuth,Intensity Value

Author: Rut Blanco (Last modification: September 2023) 
-------------------------------------------------------------------------------------------------------------------------
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





