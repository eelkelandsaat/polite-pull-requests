from os import path

'''
In this file, the paths are saved that the Python scripts in this folder work with.
'''

# Get a parent directory by file location string
parent = path.dirname

PARENT = parent(__file__)
ROOT = parent(PARENT)

WIKIPEDIA_FOLDER = path.join(PARENT, 'wikipedia_data_folder')
STACK_EXCHANGE_FOLDER = path.join(PARENT, 'stack_exchange_data_folder')
PULL_DATA_IN_FILE = path.join(ROOT, 'data', 'pull_request_data_no_bots.csv')
PULL_DATA_OUT_FILE = path.join(ROOT, 'data', 'likert_labeled_pull_messages.csv')
REGRESSOR_FOLDER = path.join(ROOT, 'regressor')
REGRESSOR_FILE = path.join(REGRESSOR_FOLDER, 'final-model.pt')