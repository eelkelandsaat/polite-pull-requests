from convokit import Corpus, download
from os import path
import random
from paths import WIKIPEDIA_FOLDER, STACK_EXCHANGE_FOLDER


TRAIN_DEV_TEST_SPLIT = .8, .1, .1

# Ensure reproducibility of the generated train/dev/test splits
random.seed(0)


# Write corpus data to a CSV file
def writeDataToCSV(dataLines: list, filePath: str):
    with open(filePath, 'w') as file:
        file.write('id,label,text\n')
        file.writelines(dataLines)


# Create CSV with format id,label,text per utterance, text being wrapped in quotes to allow for newlines inside the utterance
# trainDevTestSplits has the form tuple(num, num, num), where the nums indicate the relative sizes of the splits
def exportCorpusToCSV(corpus: Corpus, folderPath: str, trainDevTestSplit: tuple):
    # Determine split sizes
    splitsNorm = sum(trainDevTestSplit)
    numUtterances = len(corpus.get_utterance_ids())
    trainSize, devSize, _ = (int(split/splitsNorm*numUtterances) for split in trainDevTestSplit)

    # Extract CSV lines from corpus
    lines = []
    utterances = corpus.utterances
    for id, utteranceInfo in utterances.items():
        label = utteranceInfo.meta['Normalized Score']
        text = utteranceInfo.text
        textForCSV = text.replace('\'', '\'\'')
        lines.append(f'{id},{label},\'{textForCSV}\'\n')
    
    # Divide lines randomly among splits
    trainSplit = [lines.pop(random.randrange(len(lines))) for _ in range(trainSize)]
    devSplit = [lines.pop(random.randrange(len(lines))) for _ in range(devSize)]
    rest = range(len(lines))
    testSplit = [lines.pop(random.randrange(len(lines))) for _ in rest]

    # Export data to CSV files
    for split, filename in [(trainSplit, 'train.csv'), (devSplit, 'dev.csv'), (testSplit, 'test.csv')]:
        writeDataToCSV(split, path.join(folderPath, filename))


# Download the Wikipedia and Stackexchange message politeness data sets and store them in CSV files in the given folders
def createDataSets(trainDevTestSplit: tuple):
    stackExchangeCorpus = Corpus(filename=download('stack-exchange-politeness-corpus'))
    wikipediaCorpus = Corpus(filename=download('wikipedia-politeness-corpus'))

    exportCorpusToCSV(stackExchangeCorpus, STACK_EXCHANGE_FOLDER, trainDevTestSplit)
    exportCorpusToCSV(wikipediaCorpus, WIKIPEDIA_FOLDER, trainDevTestSplit)


if __name__ == '__main__':
    createDataSets(TRAIN_DEV_TEST_SPLIT)