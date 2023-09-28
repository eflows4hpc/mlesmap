# MLESmap 
This repository contains the codes needed for run the workflow of the Machine Learning Estimator for Ground Shaking Maps (MLESmap).
The MLESmap introduces an innovative approach that harnesses the predictive capabilities of Machine Learning (ML) algorithms, utilizing high-quality physics-based seismic scenarios.

## The workflow
The machine learning workflow is divided into three main stages. In the first stage, the necessary data is extracted from the seismograms and SRFs and prepared for analysis. Then, in the second stage, they reduce the features to only those relevant to the model, and the target, which is the variable they are trying to predict, in this case the intensity variable. Finally, in the third stage, the data are prepared for model training, including feature normalisation, coding of categorical variables and splitting into training and test sets. By following these stages, adequate preparation of the data for the machine learning process is ensured.

## Requirements
This project requires the following libreries. To install these libraries, it can be used the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Repository structure
The repository is organized as follows
- `Step1_Extraction.py`: the data extracted from CyberShake are processed. In this code the information is obtained from the folder post-processing of each Synthetic Station and from the file Ruptures. The output is a csv with the following information:  PGA, PGV, PSA, PSV and SD max and average, Mw, src, rv. For this step there are two different codes in the repository, one of them using PyCompss and the other one without using it.
- `Step2a_SRFExtraction.py`: In this step the data is extracted from the .srf file the information related to the earthquake hypocentre, as well as the rupture point identification and the ELON, ELAT, DTOP, SHYP, DHYP data.
- `Step2b_SRFDatabase.py`: In this step a database is generated in which the geographic coordinates of the synthetic station, the coordinates and depth of the hypocentre and the Euclidean distance and azimuth are displayed. From the file name we get the information related to the number of the synthesised station and the rupture, from the Sites file the information related to the coordinates of this station and from the srf files the information related to the earthquake. The azimuth and Euclidean distance are calculated separately.
- `Step3_Plot.py`: Extract information to plot all the results together per magnitude also including the GMPEs
- `Step4_Merge.py`: Join the databases obtained in the step 2 for each station into a general one for each PSA.
- `Step5_Concat.py`: This step is complementary to step 4. This script is in case the merge could not be done in once, so there is more than one PSA merge for each PSA.  
- `Step6_SplitIndex.py`: In this code the different event identifications per station are selected. With the four columns [Source_ID, Rupture_ID, RuptureVariation_ID, Magnitude_ID] it is intended for the separation of data with magnitude-proportional representation. With only three columns [Source_ID, Rupture_ID, RuptureVariation_ID] it is intended for random data separation..
- `Step7a_Split10Mw.py`: In this step the code loads the file obtained from the previous code to extract the unique values from the 'Magnitude' column. Then, it randomly selects 10% of the rows for each unique value of 'Magnitude'. Finally, it saves "MwData" in a new file named 10_Source_Rup_RupVar_Mw.csv .. 
- `Step7b_Split10Random.py`: In this step, the code loads the file obtained from the previous code to extract 10% of the data randomly.
A seed is added to ensure reproducibility.
Finally, save "dfRandom" in a new file named 10_Source_Rup_RupVar.csv.
- `Step8_TrainTest.py`: In this step, The code is responsible for partitioning the global database into two distinct subsets: Training database and Test database. This partitioning is based on the information obtained in the previous step. If you want to perform a random data partition, the relevant data includes [Source_ID, Rupture_ID, RuptureVariation_ID]. Alternatively, if you prefer to segregate the data based on different magnitudes, you should consider [Source_ID, Rupture_ID, RuptureVariation_ID, Magnitude]. The files containing the 10% data to be extracted are named as follows "10_Source_Rup_RupVar.csv" and "10_Source_Rup_RupVar_Mw.csv",respectively.
This process results in two different databases. The test database includes all the earthquakes corresponding to the indexes extracted above: Source_ID, Rupture_ID, RuptureVariation_ID and Magnitude. It represents approximately 10% of the total dataset. The second output, the Train database, contains information related to the remaining earthquakes.
- `Step9_DislibDatabase.py`: In this final step, all columns that would provide essential information for machine learning are retained, sorting them into necessary features and the target variable. The final column should represent the target variable.
It is advisable to transform the intensity values (PSA) into a base 10 logarithmic scale (log10). It has to be executed once for each intensity measure.
Example of features and target: Source ID,Site Lat,Site Lon,Magnitude,Hypocenter Lat,Hypocenter Lon,Hypocenter Depth, EuclideanDistance,Azimuth,Intensity Value

## Comand PyCompss
```bash
nohup pycompss run Code_PyCompss.py /path/to/data/ FolderOut &> out.out &
```
