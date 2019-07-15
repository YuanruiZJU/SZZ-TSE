# SZZ-TSE
This repository proposes the datasets and code for reproducing our paper - The Impact of Mislabeled Changes by SZZ on Just-in-Time Defect Prediction.

## How to run
* Clone the code to a directory. Running our code needs the path of the directory.
* Modify a line in the file `code/calculation/classification_importance.R`, the line is as follows:
```
# Specify the DIRECTORY path storing the code of this repository
DIR_PATH = "?" 
```
* Create the following directories in `data_results/`: `importance`, `oneway`, `results_imbalance`, `results_balance`.
* Run the script `code/calculation/classification_importance.R`

## Results
The results will be stored in `data_results/importance/`, `data_results/oneway/`,  `data_results/results_imbalance/`, `data_results/results_balance/` after running the script. We store the performance scores (e.g., auc) in each of the 1,000 bootstrap iterations into csv files.
