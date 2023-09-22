""" ALL SOURCE, RUPTURE AND RUPTURE VARIATION ID FOR ONE STATION

In this code the different event identifications per
station are selected. With the four columns [Source_ID, Rupture_ID, RuptureVariation_ID, Magnitude_ID] it is intended
for the separation of data with magnitude-proportional representation. With only three columns [Source_ID,
Rupture_ID, RuptureVariation_ID] it is intended for random data separation.

Author: Rut Blanco (Last modification September 2023) """

import pandas as pd

Site_Rup_RupVar = pd.DataFrame()
Database = pd.read_csv('/path/to/Database.csv')

Site_Rup_RupVar['Source_ID'] = Database['Source_ID']
Site_Rup_RupVar['Rupture_ID'] = Database['Rupture_ID']
Site_Rup_RupVar['RuptureVariation_ID'] = Database['RuptureVariation_ID']
Site_Rup_RupVar['Magnitude'] = Database['Magnitude']

Site_Rup_RupVar.to_csv('/data/IcelandDatabase/Source_Rup_RupVar_Mw.csv', index=False)
