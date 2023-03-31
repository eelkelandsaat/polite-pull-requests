# Do polite pull requests => faster time-to-merge ?

In this repository, you may find scripts to investigate the influence of politeness in a pull request message on its time-to-merge in medium-sized GitHub projects. To carry out the study, follow these steps:

## Obtaining pull request data (folder "request")

1. Use searchRepo.py to find repositories that meet the requirements.
2. Use these repos in mineScript.py (currently pre-filled) to obtain all the necessary pull request data from them.
3. Execute removeBots.py to remove the pull requests made by bots.

## Labelling the data (folder "label")

4. Run createDataSets.py to create the data sets to train the regression model on.
5. Run trainModel.py to train the model and store it.
6. Run assignPolitenessLabels.py to assign the labels to the data using the model and store them.

## Computing correlations (folder "computations")

7. Run coefficient.py to obtain correlation coefficients calculated directly on the present data.
8. Run coefficient_imbalanced.py to obtain correlation coefficients calculated after balancing the data using SMOTE.

This folder also contains the scripts countPulls.py and labelCounts.py. These scripts are meant for verification that the input and output data is present and sound.

## GitHub Token
Add an .env file to this directory and add your access token as follows to utilize your access token for GitHub:
```
ACCESS_TOKEN = 'your_access_token'
```
