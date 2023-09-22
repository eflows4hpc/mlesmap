""" 10% RANDOM EXTRACTION

This code loads the file obtained from the previous code to extract 10% of the data randomly.
A seed is added to ensure reproducibility.
Finally, save "dfRandom" in a new file named 10_Source_Rup_RupVar.csv.

Author: Rut Blanco Prieto (Last modified: September 2023)"""


import pandas as pd

DataIn = pd.read_csv('/path/to/Source_Rup_RupVar.csv')
DataOut = '/path/to/FolderOut/10_Source_Rup_RupVar.csv'
seed = 42

dfRandom = DataIn.sample(frac=0.10, random_state=seed)

dfRandom.to_csv(DataOut, index=False)
