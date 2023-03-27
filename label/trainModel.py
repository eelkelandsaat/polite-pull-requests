from flair.datasets import CSVClassificationCorpus
from flair.data import MultiCorpus
from flair.embeddings import TransformerDocumentEmbeddings
from flair.models.text_regression_model import TextRegressor
from flair.trainers import ModelTrainer
from paths import STACK_EXCHANGE_FOLDER, WIKIPEDIA_FOLDER, REGRESSOR_FOLDER


def trainModel():
    stackExchangeCorpus = CSVClassificationCorpus(STACK_EXCHANGE_FOLDER, column_name_map={1: 'label', 2: 'text'}, skip_header=True, label_type='regression')
    wikipediaCorpus = CSVClassificationCorpus(WIKIPEDIA_FOLDER, column_name_map={1: 'label', 2: 'text'}, skip_header=True, label_type='regression')
    totalCorpus = MultiCorpus([stackExchangeCorpus, wikipediaCorpus])

    # Initialize document embeddings
    documentEmbeddings = TransformerDocumentEmbeddings('distilbert-base-uncased', fine_tune=True)

    # Create the text regressor
    regressor = TextRegressor(documentEmbeddings, label_name='label')

    # Initialize the trainer
    trainer = ModelTrainer(regressor, totalCorpus)

    # Run training with fine-tuning
    trainer.fine_tune(REGRESSOR_FOLDER, learning_rate=5.0e-5, mini_batch_size=4, max_epochs=10)


if __name__ == '__main__':
    trainModel()