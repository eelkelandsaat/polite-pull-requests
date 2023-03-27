import requests
import os
from paths import REMOVE_BOTS_IN_FILE, REMOVE_BOTS_OUT_FILE


# Using an access token, the GitHub API allows for more requests
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

HEADERS = {
    'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
}

# For counting the number of requests to the GitHub API
counter = 0
def count(total):
    global counter
    counter += 1
    print(f'\rMaking request #{counter}/{total}', end='')


# Read a file containing pull request data, taking into account the possibility of newlines within messages
# Return a list of all the lines that contain data, including the newline characters at the end of each line
def readPullDataFile(filePath: str):
    lines = []
    with open(filePath, 'r') as inFile:
        line = inFile.readline()    # Skip the first line intentionally as it contains the column headers
        while line:
            line = inFile.readline()
            numQuotes = len(list(filter(lambda char: char == '\'', line)))
            while numQuotes % 2 == 1:
                line += inFile.readline()
                numQuotes = len(list(filter(lambda char: char == '\'', line)))
            lines.append(line)
    if lines[-1] == '\n': lines = lines[:-1]
    return lines


def removeBots(inFile: str, outFile: str):
    lines = readPullDataFile(inFile)
    num_requests = len(lines)
    with open(outFile, 'a') as file:
        for line in lines:
            url, pull_number, *_ = line.split(',')
            pull_data = requests.get(f'{url}/pulls/{pull_number}', headers=HEADERS).json()
            count(num_requests)
            if pull_data['user']['type'] == 'Bot': continue
            file.write(f'{line}')
    print('')


if __name__ == '__main__':
    removeBots(REMOVE_BOTS_IN_FILE, REMOVE_BOTS_OUT_FILE)