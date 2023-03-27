from typing import TextIO
import requests
import os
from paths import PULL_DATA_OUT_FILE


# Obtained using the searchRepo script
REPO_URLS = [
    'https://api.github.com/repos/appium/python-client',
    'https://api.github.com/repos/stanfordnlp/stanza',
    'https://api.github.com/repos/cvxpy/cvxpy',
    'https://api.github.com/repos/skulpt/skulpt',
    'https://api.github.com/repos/PyThaiNLP/pythainlp',
    'https://api.github.com/repos/cloudfoundry/python-buildpack',
    'https://api.github.com/repos/StellarCN/py-stellar-base',
    'https://api.github.com/repos/openlawlibrary/pygls',
    'https://api.github.com/repos/openai/openai-python',
    'https://api.github.com/repos/amaranth-lang/amaranth'
]

# Using an access token, the GitHub API allows for more requests
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

HEADERS = {
    'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
}


# For counting the number of requests to the GitHub API
counter = 0
def count():
    global counter
    counter += 1
    print(f'\rMaking request #{counter}', end='')


# Some pull request messages contain lengthy markdown details sections, which are not fit for assigning politeness labels.
def removeDetails(msg: str):
    detailsIdx = msg.find('<details>')
    while detailsIdx != -1:
        endIdx = msg.find('</details>')
        if endIdx == -1: return msg[:detailsIdx]
        msg = f'{msg[:detailsIdx]}{msg[endIdx + 10:]}'
        detailsIdx = msg.find('<details>')
    return msg


# Write the data of one pull request to file
def savePull(file: TextIO, pull_info: dict, repo_url: str, pull_num: int):
    created = pull_info['created']
    message = removeDetails(pull_info['message']).replace('\'', '\'\'') if pull_info['message'] else None   # For CSV compatibility, ' are represented by ''
    first_comment = pull_info['first-comment']
    first_review_comment = pull_info['first-review-comment']
    merged = pull_info['merged']
    file.write(f'{repo_url},{pull_num},{created},\'{message}\',{first_comment},{first_review_comment},{merged}\n')


# Write the data of all pull requests to file.
# error indicates whether the function call was caused by an error.
def savePulls(error: bool):
    with open(PULL_DATA_OUT_FILE, 'a') as file:
        for repo_url, pulls in repos_pulls_data.items():
            for pull_num, pull_info in pulls.items():
                savePull(file, pull_info, repo_url, pull_num)
        if error:
            for pull_num, pull_info in repo_pulls_data.items():
                savePull(file, pull_info, repo_url, pull_num)


''' repos_pulls_data is a dictionary with the following structure:
{
    <repo-url>: {
        <pull-number>: {
            'created': timestamp,
            'message': string,  (this message may contain GitHub markdown)
            'first-comment': timestamp,
            'first-review-comment': timestamp
            'merged': timestamp
        }, ...
    }
    , ...
}
'''
repos_pulls_data = {}

repo_pulls_data: dict   # Temporary variable which is iteratively added to repos_pulls_data

def minePullRequestData():
    global repos_pulls_data
    global repo_pulls_data
    try:
        for url in REPO_URLS:
            repos_pulls_data[url] = {}
            repo_pulls_data = {}
            page = 1
            pulls = requests.get(f'{url}/pulls', params = {'state': 'closed', 'per_page': 100, 'page': page}, headers=HEADERS).json()
            while pulls:
                print(f'\nRepo: {url}\nPull requests: {len(pulls)}')
                count()
                for pull in pulls:
                    if not pull['merged_at']: continue  # Pull request was not merged
                    
                    # Get relevant data
                    pull_number = pull['number']
                    comments = requests.get(f'{url}/issues/{pull_number}/comments', headers=HEADERS).json()
                    count()
                    review_comments = requests.get(f'{url}/pulls/{pull_number}/comments', headers=HEADERS).json()
                    count()
                    first_comment = comments[0]['created_at'] if comments else None
                    first_review_comment = review_comments[0]['created_at'] if review_comments else None
                    
                    # Store relevant data
                    repo_pulls_data[pull_number] = {
                        'created': pull['created_at'],
                        'message': pull['body'] if 'body' in pull else None,
                        'first-comment': first_comment,
                        'first-review-comment': first_review_comment,
                        'merged': pull['merged_at']
                    }
                    page += 1
                    pulls = requests.get(f'{url}/pulls', params = {'state': 'closed', 'per_page': 100, 'page': page}, headers=HEADERS).json()
            # Accumulate
            repos_pulls_data[url] = repo_pulls_data
    except BaseException as e:
        print(f'\nAn error occured: \'{type(e).__name__}: {e}\'. Saving gathered data.')
        savePulls(error=True)
    else:
        print(f'\nExecution successful. Saving gathered data.')
        savePulls(error=False)


if __name__ == '__main__':
    minePullRequestData()