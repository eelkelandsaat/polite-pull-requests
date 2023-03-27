from flair.models.text_regression_model import TextRegressor
from flair.data import Sentence
from paths import PULL_DATA_IN_FILE, PULL_DATA_OUT_FILE, REGRESSOR_FILE


# For assigning class-labels in the set {-1, 0, 1}
def regressionToClassLabel(regressionScore: float) -> int:
    if regressionScore < -0.5: return -1
    if regressionScore < 0.5: return 0
    return 1


# Take a regression score and return its corresponding Likert score (from the set {1, 2, 3, 4, 5})
def regressionToLikertLabel(regressionScore: float) -> int:
    if regressionScore < -0.75: return 1
    if regressionScore < -0.25: return 2
    if regressionScore < 0.25: return 3
    if regressionScore < 0.75: return 4
    return 5


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
    lines = list(filter(lambda line: line not in '\n', lines))  # Also handles empty lines
    return lines


# Read all the messages in a file containing pull request data
# Only works if all messages are surrounded by quotation marks in the file (e.g., not plain None)
# Return a dictionary of repo URLs to dictionaries of pull numbers to messages
def getPullRequestMessages(filePath: str):
    res = {}
    lines = readPullDataFile(filePath)
    for line in lines:
        msgStart = line.find('\'')
        msgEnd = len(line) - line[::-1].find('\'')
        msg = line[msgStart:msgEnd]     # Message with surrounding quotation marks included
        url, pullNumber, _ = line.split(',', maxsplit=2)
        if url not in res: res[url] = {}
        res[url][pullNumber] = msg
    return res


# Read pull request data from inFileLoc and regress the messages using the model at regressorLoc.
# Write the result of taking the regression score to labelMethod to outFileLoc, which is created if it does not exist yet.
def assignPolitenessLabels(inFileLoc: str, outFileLoc: str, regressorLoc: str, labelMethod: callable):
    model = TextRegressor.load(regressorLoc)

    # Dictionary of repo URLs to dictionaries of pull numbers to messages
    messages = getPullRequestMessages(inFileLoc)

    # Dictionary of repo URLs to lists of pull number, message, regression score, classification label tuples
    regAndClassLabels = {}

    for url, msgDict in messages.items():
        repoPulls = []
        repoSentences = []
        for pullNumber, msg in msgDict.items():
            repoPulls.append(pullNumber)
            repoSentences.append(Sentence(msg))
        model.predict(repoSentences)
        regAndClassLabels[url] = [(pullNo, sentence, float(sentence.tag), labelMethod(float(sentence.tag))) for pullNo, sentence in zip(repoPulls, repoSentences)]

    with open(outFileLoc, 'w') as outFile:
        outFile.write('repo_api_url,pull_number,regression_score,class_label,message\n')
        for url, pullList in regAndClassLabels.items():
            outFile.writelines([f'{url},{pullNo},{regressionLabel},{classLabel},{sentence.to_original_text()}\n' for pullNo, sentence, regressionLabel, classLabel in pullList])


if __name__ == '__main__':
    assignPolitenessLabels(PULL_DATA_IN_FILE, PULL_DATA_OUT_FILE, REGRESSOR_FILE, labelMethod=regressionToLikertLabel)