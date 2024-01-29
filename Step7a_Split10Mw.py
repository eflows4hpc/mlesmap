""" 10% PER MAGNITUDE EXTRACTION

This code loads the file obtained from the previous code to extract the unique values from the 'Magnitude' column.
Then, it randomly selects 10% of the rows for each unique value of 'Magnitude'.
Finally, it saves "MwData" in a new file named 10_Source_Rup_RupVar_Mw.csv .

Author: Rut Blanco Prieto (Last modified: September 2023)
-------------------------------------------------------------------------------------------------------------------
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
