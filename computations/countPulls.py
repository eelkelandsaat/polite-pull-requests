from paths import PULL_DATA_FILE

'''
This script counts the number of pull requests in the given CSV file.
'''

lines = []
with open(PULL_DATA_FILE, 'r') as inFile:
    line = inFile.readline()    # Skip the first line intentionally
    while line:
        line = inFile.readline()
        numQuotes = len(list(filter(lambda char: char == '\'', line)))
        while numQuotes % 2 == 1:
            line += inFile.readline()
            numQuotes = len(list(filter(lambda char: char == '\'', line)))
        lines.append(line)
lines = lines[:-1]
print(f'Num pulls: {len(lines)}')