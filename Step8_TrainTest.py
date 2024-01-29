""" TRAIN AND TEST DATABASES

The code is responsible for partitioning the global database into two distinct
subsets: Training database and Test database. This partitioning is based on the information obtained in the previous
step. If you want to perform a random data partition, the relevant data includes [Source_ID, Rupture_ID,
RuptureVariation_ID]. Alternatively, if you prefer to segregate the data based on different magnitudes, you should
consider [Source_ID, Rupture_ID, RuptureVariation_ID, Magnitude]. The files containing the 10% data to be extracted
are named as follows "10_Source_Rup_RupVar.csv" and "10_Source_Rup_RupVar_Mw.csv", respectively.

This process results in two different databases. The test database includes all the earthquakes corresponding to the
indexes extracted above: Source_ID, Rupture_ID, RuptureVariation_ID and Magnitude. It represents approximately 10% of
the total dataset. The second output, the Train database, contains information related to the remaining earthquakes.

Author: Rut Blanco (Last modification: September 2023) 
----------------------------------------------------------------------------------------------------------------------
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

# PASO 1 TEST
df10Selected = pd.read_csv('/path/to/10%selected/10_Source_Rup_RupVar_Mw.csv')
Database = pd.read_csv('/path/to/Database.csv')

DataOut1 = '/path/to/FolderOut/Test.csv'
DataOut2 = '/path/to/FolderOut/Train.csv'

dfEQ = pd.merge(Database, df10Selected, on=['Source ID', 'Rupture ID', 'Rupture Variation ID', 'Magnitude'],
                how='inner')
dfEQ.to_csv(DataOut1, index=False)

# PASO 2 TRAIN
chunk_size = 600000
chunks = pd.read_csv('/path/to/Database.csv', chunksize=chunk_size)
DataOut1 = pd.read_csv('/path/to/Test.csv')

TrainChunks = []
for chunk in chunks:
    chunk_df = chunk

    df = pd.merge(chunk_df, DataOut1, on=['Source ID', 'Rupture ID', 'Rupture Variation ID', 'Magnitude'], how='left')
    merged = chunk_df.merge(DataOut1, how='left', indicator=True)  # left,right,both

    dfNotEQ = merged[merged['_merge'] == 'left_only']  # in the merge column, only those listed as left_only
    dfNotEQ = dfNotEQ.drop('_merge', axis=1)

    TrainChunks.append(dfNotEQ)

Train = pd.concat(TrainChunks, ignore_index=True)
Train.to_csv(DataOut2, index=False)
