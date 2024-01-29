""" ALL SOURCE, RUPTURE AND RUPTURE VARIATION ID FOR ONE STATION

In this code the different event identifications per
station are selected. With the four columns [Source_ID, Rupture_ID, RuptureVariation_ID, Magnitude_ID] it is intended
for the separation of data with magnitude-proportional representation. With only three columns [Source_ID,
Rupture_ID, RuptureVariation_ID] it is intended for random data separation.

Author: Rut Blanco (Last modification September 2023) 
-----------------------------------------------------------------------------------------------------------------------
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

Site_Rup_RupVar = pd.DataFrame()
Database = pd.read_csv('/path/to/Database.csv')

Site_Rup_RupVar['Source_ID'] = Database['Source_ID']
Site_Rup_RupVar['Rupture_ID'] = Database['Rupture_ID']
Site_Rup_RupVar['RuptureVariation_ID'] = Database['RuptureVariation_ID']
Site_Rup_RupVar['Magnitude'] = Database['Magnitude']

Site_Rup_RupVar.to_csv('/data/IcelandDatabase/Source_Rup_RupVar_Mw.csv', index=False)
