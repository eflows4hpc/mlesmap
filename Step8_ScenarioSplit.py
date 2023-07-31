'''
STEP 7.3: SPLIT DATA BY SCENARIO
In this step, once the database is prepared for Dislib, the data is divided between Train and Test.
For this purpose, in the general database, the data with the same earthquake hypocentre coordinates are combined and its extracted the 5% of each scenario.
'''

import numpy as np
import pandas as pd
import os

PSA = pd.read_csv('/path/data/dislib_database_period.csv')

#Group the data by the information of the hypocenter of the event
agrupados = PSA.groupby(['Hypocenter Lat', 'Hypocenter Lon', 'Hypocenter Depth'])

#List for storing the indexes of extracted rows
extracted_indices = []

#Function to draw a 5% random sample from each group and store the rows and indices.
def extract_random_sample(group):
    sample_size = int(len(group) * 0.05) 
    sample = group.sample(n=sample_size)
    extracted_indices.extend(sample.index.tolist())  # Agregar los índices a la lista
    sample.to_csv(os.path.join(output_dir, 'Scenario_Test3s.csv'), mode='a', header=False, index=False)

#Output directory
output_dir = '/data/database/DislibDatabase/'

#.csv file to save extracted rows
with open(os.path.join(output_dir, 'Scenario_Test3s.csv'), 'w') as f:
    pass

#Extract a 5% random sample from each group and save the rows and indices.
agrupados.apply(extract_random_sample)

#.csv file to save extracted index
extracted_indices_df = pd.DataFrame({'Index': extracted_indices})
extracted_indices_df.to_csv(os.path.join(output_dir, 'ScenarioVector3s.csv'), index=False)

#.csv file to save non "selected" rows
non_selected_rows = PSA[~PSA.index.isin(extracted_indices)]
non_selected_rows.to_csv(os.path.join(output_dir, 'Scenario_Train3s.csv'), index=False)