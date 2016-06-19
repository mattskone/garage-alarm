import logging
import pickle
from sklearn import cross_validation, svm
import config
import samples

logger = logging.getLogger(__name__)


def get_trained_model():
    return pickle.load(open(config.MODEL_FILE_NAME))


def train_model():
    logger.info('Training new model')
    training_samples, training_labels = samples.get_samples(
        config.POSITIVE_SAMPLE_DIR,
        config.NEGATIVE_SAMPLE_DIR)
    model = svm.SVC(kernel='linear')
    model.fit(training_samples, training_labels)
    with open(config.MODEL_FILE_NAME, 'w') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    train_model()

