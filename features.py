import os
import cv2
import numpy as np


def get_features_for_image(file_path):
    # Get grayscale image, normalized to 0.0-1.0 
    raw = cv2.imread(file_path, 0) * (1 / 255.0)
    return raw.flatten()


def get_features(dir_path, file_extension='jpg'):
    """Extract the features for all images in a directory.

    :param dir_path: path to the directory where image files can be found
    :type file_path: str.
    :param extension: the image files extension
    :returns: a 2D numpy matrix of image features
    """

    files = [name for name in os.listdir(dir_path) if name.endswith(file_extension)]
    features = []
    for f in files:
        features.append(get_features_for_image(os.path.join(dir_path, f)))

    return np.array(features)

