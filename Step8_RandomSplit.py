'''
STEP 7.1: SPLIT DATA BY RANDOM
In this step, once the database is prepared for Dislib, the data is divided between Train and Test.
For this purpose, in the general database, 10% of the data is randomly extracted.
One execution is needed for each PSA.
'''

import numpy as np
import pandas as pd
import os


PSA = pd.read_csv('/path/data/dislib_database_period.csv')

total_row = PSA.shape[0]
total_row

#To allow reproducibility
np.random.seed(12)

output_dir = '/data/database/DislibDatabase/'

#Extraction of 10% of the database on a random basis
extract_row = int(total_row * 0.1)
random_extraction = PSA.sample(n=extract_row)
random_extraction.to_csv(os.path.join(output_dir,'Dislib_RandomTest5s.csv'), index=False)

#Identification of randomly separated rows for Test
index_row_extraction = random_extraction.index.values
print("Index of the rows randomly extracted:", index_row_extraction)

#Extraction of these indices as a vector
num_elementos = len(index_row_extraction)
index_row_extraction_list = index_row_extraction.tolist()
num_elementos_df = pd.DataFrame({'num_elementos': [index_row_extraction_list]})
num_elementos_df.to_csv(os.path.join(output_dir, 'RandomVector5s.csv'), index=False)
print("The vector has", num_elementos, "elements.")

#Extract the rest of the elements in a database for Train
non_selected_rows = PSA[~PSA.index.isin(random_extraction.index)]
non_selected_rows.to_csv(os.path.join(output_dir,'Dislib_RandomTrain5s.csv'), index=False)
