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
- `Step2_SRFExtraction.py`: In this step a database is generated in which the geographic coordinates of the synthetic station, the coordinates and depth of the hypocentre and the Euclidean distance and azimuth are displayed. From the file name we get the information related to the number of the synthesised station and the rupture, from the Sites file the information related to the coordinates of this station and from the srf files the information related to the earthquake. The azimuth and Euclidean distance are calculated separately.
- `Step3_Plot.py`: Extract information to plot all the results together per magnitude also including the GMPEs
- `Step4_Merge.py`: Join the databases obtained in the step 2 for each station into a general one for each PSA.
- `Step5_Concat.py`: This step is complementary to step 4. This script is in case the merge could not be done in once, so there is more than one PSA merge for each PSA. 
- `Step6_Dislib.py`: Data preparation for Dislib, in this step the database is filtered with only the necessary features and target. 
- `Step7_DropNaN.py`: This step is not entirely necessary, it is just to ensure that there are no incomplete rows or no data.
- `Step8a_SplitMagnitude.py`: In this step, once the database is prepared for Dislib, the data is divided between Train and Test.
For this purpose, in the general database, the data with the same earthquake hypocentre coordinates are combined and the magnitude data are separated proportionally to the presence. 
- `Step8b_SplitRandom.py`: In this step, once the database is prepared for Dislib, the data is divided between Train and Test. For this purpose, from the general database, 10% of the data is randomly extracted.
- `Step8c_SplitScenario.py`: In this step, once the database is prepared for Dislib, the data is divided between Train and Test. For this purpose, from the general database, the data with the same earthquake hypocentre coordinates are combined and its extracted the 5% of each scenario.
