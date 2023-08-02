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
- `Step1_Extraction.py`: the data extracted from CyberShake are processed. 
- `Step2_SRFExtraction.py`: a database is generated in which the geographic coordinates of the synthetic station, the coordinates and depth of the hypocentre and the Euclidean distance and azimuth are displayed.
- `Step3_Plot.py`: 
- `Step4_Merge.py`: Join the databases obtained in the step 2 for each station into a general one for each PSA.
- `Step5_Concat.py`: This script is in case the merge could not be done in once, so there is more than one PSA merge for each PSA.
- `Step6_Dislib.py`: Data preparation for Dislib
- `Step7_DropNaN.py`: Drop duplicate or empty rows.
- `Step8a_SplitMagnitude.py`: The data is divided between Train and Test in proportion to the number of rows per magnitude in each scenario.
- `Step8b_SplitRandom.py`: The data is divided between Train and Test randomly from the general database.
- `Step8c_SplitScenario.py`: The data is split between Train and Test randomly from each scenario.
