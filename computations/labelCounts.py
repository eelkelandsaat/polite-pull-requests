from collections import Counter
from paths import LABELS_FILE, LIKERT_LABELS_FILE

'''
This script counts the label distributions in the given CSV files. It should not be used for regression labels.
'''


def hasMessage(split):
    return split[4] != 'None'


lines: list[str]
with open(LABELS_FILE, 'r') as file:
    lines = file.readlines()[1:-1]

splits = [line.split(',', maxsplit=4) for line in lines]
splits = [[url, int(pullNo), float(regScore), int(classLabel), msg[1:-2]] for url, pullNo, regScore, classLabel, msg in splits]
politeCount = len(list(filter(lambda split: hasMessage(split) and split[3] == 1, splits)))
neutralCount = len(list(filter(lambda split: hasMessage(split) and split[3] == 0, splits)))
rudeCount = len(list(filter(lambda split: hasMessage(split) and split[3] == -1, splits)))
print(f'Rude #:    {rudeCount}')
print(f'Neutral #: {neutralCount}')
print(f'Polite #:  {politeCount}\n')

with open(LIKERT_LABELS_FILE, 'r') as file:
    lines = file.readlines()[1:-1]

splits = [line.split(',', maxsplit=4) for line in lines]
splits = [[url, int(pullNo), float(regScore), int(classLabel), msg[1:-2]] for url, pullNo, regScore, classLabel, msg in splits]
labels = [int(likertLabel) for _, _, _, likertLabel, msg in splits if msg != 'None']
counts = Counter(labels)
print('Likert labels:')
for label in range(1, 6):
    print(f'{label}:         {counts[label]}')

print(f'\nTotal # pulls with a message: {len(lines)}')