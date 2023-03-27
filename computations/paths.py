from os import path

'''
In this file, the paths are saved that the Python scripts in this folder work with.
'''

# Get a parent directory by file location string
parent = path.dirname

ROOT = parent(parent(__file__))

LABELS_FILE = path.join(ROOT, 'data', 'labeled_pull_messages.csv')
LIKERT_LABELS_FILE = path.join(ROOT, 'data', 'likert_labeled_pull_messages.csv')
PULL_DATA_FILE = path.join(ROOT, 'data', 'pull_request_data_no_bots.csv')