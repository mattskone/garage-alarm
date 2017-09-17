"""
A module to return a trained model.

This module can be invoked manually to train a new model from existing samples.
$ python ./models.py
"""

import logging
import os
import pickle
from sklearn import svm
from sklearn.cross_validation import cross_val_score
import config
import samples

logger = logging.getLogger(__name__)


def get_trained_model(use_current=True):
    """Return a trained classifier."""

    if use_current:
        return pickle.load(open(os.path.join(config.INSTALL_DIR,
                                             config.MODEL_FILE_NAME)))
    else:
        return _get_new_trained_model()


def _get_new_trained_model():
    logger.info('Training new model')
    training_samples, training_labels = samples.get_samples(
        os.path.join(config.INSTALL_DIR, config.POSITIVE_SAMPLE_DIR),
        os.path.join(config.INSTALL_DIR, config.NEGATIVE_SAMPLE_DIR))
    model = svm.SVC(kernel='linear')
    _score_model(model, training_samples, training_labels)
    logger.info('Fitting new model')
    model.fit(training_samples, training_labels)

    return model


def _score_model(model, samples, labels):
    print 'Scoring model...'
    scores = cross_val_score(model, samples, labels, cv=5)
    print 'Model accuracy score: {0:0.2f}'.format(scores.mean())


if __name__ == '__main__':
    model = get_trained_model(False)
    with open(os.path.join(config.INSTALL_DIR, config.MODEL_FILE_NAME), 'w') as f:
        pickle.dump(model, f)

