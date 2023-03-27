from os import path

'''
In this file, the paths are saved that the Python scripts in this folder work with.
'''

# Get a parent directory by file location string
parent = path.dirname

ROOT = parent(parent(__file__))

PULL_DATA_OUT_FILE = REMOVE_BOTS_IN_FILE = path.join(ROOT, 'data', 'pull_request_data.csv')
REMOVE_BOTS_OUT_FILE = path.join(ROOT, 'data', 'pull_request_data_no_bots.csv')