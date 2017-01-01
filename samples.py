import argparse
import logging
import os

import numpy as np
from sklearn.utils import shuffle

import camera
import config
import features


logger = logging.getLogger(__name__)


def get_samples(pos_samples_dir, neg_samples_dir, reduced=False):
    """Produce sample data ready for training a classifier.

    :param pos_samples_dir: path to directory containing positive samples
    :param neg_samples_dir: path to directory containing negative samples
    :param reduced: when True, apply dimensionality reduction to the samples
    :returns: two numpy arrays.  The first (x, f) contains the feature data for
        x samples, and the second (y, ) contains the classifications for each
        of the samples.
    """

    logger.info('Getting training samples')
    pos_samples = features.get_features_for_dir(pos_samples_dir)
    pos_classes = np.ones(pos_samples.shape[0])
    neg_samples = features.get_features_for_dir(neg_samples_dir)
    neg_classes = np.zeros(neg_samples.shape[0])
    samples = np.vstack([pos_samples, neg_samples])
    if reduced:
        samples = features.reduce_features(samples, False)
    classes = np.hstack([pos_classes, neg_classes])
    samples, classes = shuffle(samples, classes)
    logger.info('Got training samples')

    return samples, classes


def take_sample(pos_sample):
    """"Take a new sample for use in training.

    :param pos_sample: when True, store the captured image as a positive sample
    """

    if pos_sample:
        sample_dir = os.path.join(config.INSTALL_DIR,
                                  config.POSITIVE_SAMPLE_DIR)
    else:
        sample_dir = os.path.join(config.INSTALL_DIR,
                                  config.NEGATIVE_SAMPLE_DIR)
    c = camera.Camera(sample_dir)
    c.take_photo()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('--positive',
                             dest='pos_sample',
                             action='store_true',
                             help='Set for positive samples')
    mutex_group.add_argument('--negative',
                             dest='pos_sample',
                             action='store_false',
                             help='Set for negative samples')
    args=parser.parse_args()
    take_sample(args.pos_sample)

