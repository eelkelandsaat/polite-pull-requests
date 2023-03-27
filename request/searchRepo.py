import os, requests
from dotenv import load_dotenv
from datetime import datetime


# Init
load_dotenv()

# Using an access token, the GitHub API allows for more requests
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

HEADERS = {
    'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
}


# Check for our requirements
def checkReqs(repo):
    # Checks for PR
    pulls = requests.get('{}?{}'.format(repo['pulls_url'][:-9], 'state=closed&per_page=1'), headers=HEADERS)
    if pulls.json() == []:
        return False, None, None
    
    totalPulls = 0
    cnt = 0
    for s in reversed(pulls.headers['Link'][:-13]):
        if s == '=':
            break
        totalPulls += int(s)*pow(10, cnt)
        cnt += 1
    if totalPulls < 100:
        return False, None, None

    # Checks for contributors
    contributors = requests.get('{}?{}'.format(repo['contributors_url'], 'anon=1&per_page=1'), headers=HEADERS)
    if contributors.json() == []:
        return False, None, None
    
    totalContributors = 0
    cnt = 0
    for s in reversed(contributors.headers['Link'][:-13]):
        if s == '=':
            break
        totalContributors += int(s)*pow(10, cnt)
        cnt += 1
    if totalContributors < 20:
        return False, None, None

    # Checks for PR date
    pullsDate = requests.get('{}?{}'.format(repo['pulls_url'][:-9], 'state=closed&per_page=100'), headers=HEADERS)
    lastYear = datetime.strptime(pullsDate.json()[24]['created_at'], '%Y-%m-%dT%H:%M:%SZ') > datetime(2022,1,24)
    lastTenYears = datetime.strptime(pullsDate.json()[99]['created_at'], '%Y-%m-%dT%H:%M:%SZ') > datetime(2013,1,24)

    return (lastYear and lastTenYears), totalPulls, totalContributors


# Search for 10 repos on GitHub that meet the project's requirements and print them.
def searchRepos():
    # Search
    repos = requests.get(
        'https://api.github.com/search/repositories?q={}'.format(
        'language=python&size=>3000&pushed=>2023-01-15&is=public'
        ), headers=HEADERS)

    # Test for requirements, until 10 repos are found
    accepted = []
    for repo in repos.json()['items']:
        accept, totalPulls, totalContributors = checkReqs(repo)
        if accept:
            print('Hit!')
            accepted.append({
                'repository' : repo['name'],
                'url' : repo['url'],
                'html_url' : repo['html_url'],
                'pulls' : totalPulls,
                'contributors' : totalContributors
            })
        if len(accepted) == 10:
            break

    # Print accepted
    print('\n\nYou should consider:')
    for idx, repo in enumerate(accepted):
        print(
            ' {}:{}\n  html: {}\n  pulls: {}\n  contributors: {}'.format(
            idx+1, repo['repository'], repo['html_url'], repo['pulls'], repo['contributors']
            ))


if __name__ == '__main__':
    searchRepos()