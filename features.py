import logging
import os
import pickle
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA


def _get_reducer(features, use_current=True):
    """Return a dimensionality reducer trained on the input samples

    :param features: a 2d numpy array of features
    :param n_components: reduce the original number of features to this amount
    :param use_current: when True, use the existing reducer instead of fitting
        a new one.  Default True.
    :returns: an instance of a scikit-learn PCA reducer
    """

    if use_current:
        return pickle.load(open(os.path.join(config.INSTALL_DIR,
                                             config.REDUCER_FILE_NAME)))
    else:
        return _get_new_reducer(features)


def _get_new_reducer(features, n_components=100):
    pca = PCA(n_components=n_components)
    return pca.fit(features)


def get_features_for_image(file_path):
    """Extract the features for a specific image.

    :param file_path: path to and name of image file
    :returns: a 2D numpy array of image features of shape (1, num_features)

    The features returned are the greyscale image intensities for each pixel,
    normalized to 0.0-1.0.
    """

    raw = Image.open(file_path).convert('L')
    normalized = np.array(raw.getdata()) * (1 / 255.0)
    normalized_2d = normalized.reshape(1, normalized.size)

    return normalized_2d 


def reduce_features(features, use_current=True):
    """Apply dimensionality reduction to feature matrix

    :param features: a 2d numpy array of sample features
    :param use_current: when True, use the existing reducer instead of fitting
        a new one.  Default True.
     :returns: a 2d numpy array of features reduced by the reducer function
    """

    reducer = _get_reducer(features, use_current)
    with open('reducer.pkl', 'w') as f:
        pickle.dump(reducer, f)
    features = reducer.transform(features)

    return features


def get_features_for_dir(dir_path, file_extension='jpg'):
    """Extract the features for all images in a directory.

    :param dir_path: path to the directory where image files can be found
    :param file_extension: the image files extension
    :returns: a 2D numpy array of image features
    """

    files = [name for name in os.listdir(dir_path) if name.endswith(file_extension)]
    features = []
    for f in files:
        features.append(get_features_for_image(os.path.join(dir_path, f)))

    return np.array(features)

