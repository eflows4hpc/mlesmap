'''
STEP 5: CONCAT

This step is complementary to step 4. This script is in case the merge could not be done in once, so there is more than one PSA merge for each PSA. 
This step is also useful in case there is an empty row.
'''

import pandas as pd

#.csv merge files for concat
file1_path = '/path/to/merge1.csv'
file2_path = '/path/to/merge2.csv'
file3_path = '/path/to/merge3.csv'
file4_path = '/path/to/merge4.csv'
file5_path = '/path/to/merge5.csv'

#Output file
output_path = '/path/output/Database_period.csv'  

#Read .csv files
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)
df3 = pd.read_csv(file3_path)
df4 = pd.read_csv(file4_path)
df5 = pd.read_csv(file5_path)

#Concat dataframes
concatenated_df = pd.concat([df1, df2, df3, df4, df5])

#Save in a .csv
concatenated_df.to_csv(output_path, index=False)
