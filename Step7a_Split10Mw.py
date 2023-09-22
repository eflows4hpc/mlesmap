""" 10% PER MAGNITUDE EXTRACTION

This code loads the file obtained from the previous code to extract the unique values from the 'Magnitude' column.
Then, it randomly selects 10% of the rows for each unique value of 'Magnitude'.
Finally, it saves "MwData" in a new file named 10_Source_Rup_RupVar_Mw.csv .

Author: Rut Blanco Prieto (Last modified: September 2023)"""

import pandas as pd
import random

Database = pd.read_csv('/path/to/Source_Rup_RupVar_Mw.csv')
unique_magnitudes = Database['Magnitude'].unique()  # Magnitude unique values

MwData = pd.DataFrame()  # Dataframe for magnitude

for magnitude in unique_magnitudes:  # Iterate through each unique value of 'Magnitude'

    subset = Database[Database['Magnitude'] == magnitude]  # Filter Database to get the rows with the current magnitude
    num_samples = int(0.10 * len(subset))
    random_subset = subset.sample(n=num_samples, random_state=42)  # Seed

    MwData = pd.concat([MwData, random_subset])

MwData.to_csv('/path/to/FolderOut/10_Source_Rup_RupVar_Mw.csv', index=False)
