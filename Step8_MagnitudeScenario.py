'''
STEP 8.1: SPLIT DATA BY SCENARIO AND MAGNITUDE
In this step, once the database is prepared for Dislib, the data is divided between Train and Test.
For this purpose, in the general database, the data with the same earthquake hypocentre coordinates are combined and the magnitude data are separated proportionally to the presence.
One execution is needed for each PSA.
'''

import numpy as np
import pandas as pd
import os


PSA = pd.read_csv('/path/data/Database_period.csv')

# Group the data by the information of the hypocenter and the magnitude of the event
agrupados = PSA.groupby(['Hypocenter Lat', 'Hypocenter Lon', 'Hypocenter Depth', 'Magnitude'])

# List for storing the indexes of extracted rows
extracted_indices = []

# Function to draw a 10% random sample from each group and store the rows and indices.
def extract_random_sample(group):
    sample_size = int(len(group) * 0.1)  # Size: 10% of the total size of the group
    sample = group.sample(n=sample_size)
    extracted_indices.extend(sample.index.tolist()) 
    sample.to_csv(os.path.join(output_dir, 'MagnitudeScenario_Test5s.csv'), mode='a', header=False, index=False)

# Output directory
output_dir = '/path/data/DislibDatabase/'

# .csv containing the extracted indices
extracted_indices_df = pd.DataFrame({'Index': extracted_indices})
extracted_indices_df.to_csv(os.path.join(output_dir, 'MagnitudeScenarioVector5s.csv'), index=False)

# .csv with the non "selected" rows
non_selected_rows = PSA[~PSA.index.isin(extracted_indices)]
non_selected_rows.to_csv(os.path.join(output_dir, 'MagnitudeScenario_Train5s.csv'), index=False)
