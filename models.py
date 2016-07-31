import logging
import os
import pickle
from sklearn import cross_validation, svm
import config
import samples

logger = logging.getLogger(__name__)


def get_trained_model(use_current=True):
    if use_current:
        return pickle.load(open(os.path.join(config.INSTALL_DIR,
                                             config.MODEL_FILE_NAME)))
    else:
        return _get_new_trained_model()


def _get_new_trained_model():
    print 'Training new model'
    training_samples, training_labels = samples.get_samples(
        os.path.join(config.INSTALL_DIR, config.POSITIVE_SAMPLE_DIR),
        os.path.join(config.INSTALL_DIR, config.NEGATIVE_SAMPLE_DIR))
    model = svm.SVC(kernel='linear')
    print 'Fitting model'
    model.fit(training_samples, training_labels)

    return model


if __name__ == '__main__':
    model = get_trained_model(False)
    with open(os.path.join(config.INSTALL_DIR, config.MODEL_FILE_NAME), 'w') as f:
        pickle.dump(model, f)

