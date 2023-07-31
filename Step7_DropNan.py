'''
STEP 7: DROP NaN 
This step is not entirely necessary, it is just to ensure that there are no incomplete rows or no data.
'''

import pandas as pd
input_path = '/input/path/Database_period.csv'
output_path = '/output/path/Database_period.csv' 

# Read CSV
df1 = pd.read_csv(input_path)


# Drop NaN
concatenated_df = df1.dropna()

concatenated_df.to_csv(output_path, index=False)
