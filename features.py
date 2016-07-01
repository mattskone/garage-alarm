import logging
import os
import numpy as np
from PIL import Image


logger = logging.getLogger(__name__)


def get_features_for_image(file_path):
    """Extract the features for a specific image.

    :param file_path: path to and name of image file
    :returns: a 2D numpy array of image features
    """

    # Get grayscale image, normalized to 0.0-1.0 
    raw = Image.open(file_path).convert('L')
    normalized = np.array(raw.getdata()) * (1 / 255.0)

    return normalized


def get_features(dir_path, file_extension='jpg'):
    """Extract the features for all images in a directory.

    :param dir_path: path to the directory where image files can be found
    :param file_extension: the image files extension
    :returns: a 2D numpy array of image features
    """

    logger.info('Getting training sample features')
    files = [name for name in os.listdir(dir_path) if name.endswith(file_extension)]
    features = []
    for f in files:
        features.append(get_features_for_image(os.path.join(dir_path, f)))
    logger.info('Got training sample features')

    return np.array(features)

