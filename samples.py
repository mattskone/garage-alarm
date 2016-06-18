import numpy as np
from sklearn.utils import shuffle
import features


def get_samples(pos_samples_dir, neg_samples_dir):
    pos_samples = features.get_features(pos_samples_dir)
    pos_classes = np.ones(pos_samples.shape[0])
    neg_samples = features.get_features(neg_samples_dir)
    neg_classes = np.zeros(neg_samples.shape[0])
    samples = np.vstack([pos_samples, neg_samples])
    classes = np.hstack([pos_classes, neg_classes])
    samples, classes = shuffle(samples, classes)

    return samples, classes

