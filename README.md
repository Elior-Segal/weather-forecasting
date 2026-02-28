# Weather Forecasting

This is my data science project git repository.\
In this project I predict whether it's going to rain in the following day on various locations in Australia.

## Project Structure
* The main file is the Jupyter notebook WeatherPrediction.ipynb.
* Other code files, which mainly used to parse and download enriched data, are in the src directory.
* Also, the additional downloaded and parsed data are in the src/resources directory.
* The python dependencies are described in the requirements.txt file
* The optuna_db directory contains sql dbs of the Optuna studies I ruan.

## Project Methodology and Report
The PDF contains the methodology and my research choices.\
The 2 PDFs are the same except one of them contains comments about what information was added after the presentations.
### Important Note:
The results are slightly different from the results presented in the presentations.\
This is mainly because of a:
1. More organized workflow.
2. In the presentations I accidentally dropped the cloud columns.
3. (Because of the above) I chose different iterative imputer in order to impute the missing values.

## Skip Sections by Preprocessed Data
Some of the code is for preprocessing and preparing data,
Therefore, technically it can be skipped to save run time or run only parts of the code instead of everything.\
The following sections describe the preprocessing execution order and what resource if present allows to skip this step:

### Data Enrichments
The python code files in the src directory download and parse additional data from the website.\
get_evaporation tackles evaporation, get_solar_exposure tackles sunshine and stations_parser tackles stations.txt.\
But if their resources are present no need to run them manually.

### Imputed Dataframes
I save the dataframes after the imputation steps in order to be able to skip the imputation step again and again.\
The "Simple data engineering and null handling" section in the notebook is used to compute the df_imputed_knn_random_forest.pkl dataframe.\
The "Let's Impute Sunshine!" and "Let's impute Evaporation" sections in the notebook are used to compute the df_imputed_final.pkl dataframe.\
Those sections can be skipped if the pickle files already exist.

### Optuna DBs
In the Hyperparameter tuning and LSTM sections are Optuna studies which takes a long time to complete.\
But the studies are kept on storage in the optuna_dbs directory, so if the db is present, running the study will be skipped automatically.

## Runtime
I ran the notebook locally which means the runtime and cells output might be slightly different on other platforms.\
I added a "# Time warning:" comment on cells which might take a long run time.\
Note: ExtraTrees as an iterative imputer estimator seems to take too much memory on Google collab.
So, I highly recommend commenting it out in the cell commented with "MEMORY WARNING".
