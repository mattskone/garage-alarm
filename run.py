import os
import numpy as np
from sklearn import cross_validation, grid_search, svm
import camera
import classifiers
import features
import samples
import shutil


POSITIVE_SAMPLE_DIR = 'samples/positive'
NEGATIVE_SAMPLE_DIR = 'samples/negative'
NEW_TRIAL_DIR = 'trials'
POSITIVE_TRIAL_DIR = 'trials/positive'
NEGATIVE_TRIAL_DIR = 'trials/negative'


def main():
    x, y = samples.get_samples(POSITIVE_SAMPLE_DIR,
                               NEGATIVE_SAMPLE_DIR) 
    classifier = classifiers.get_trained_classifier(x, y)
    new_trial_file_name = camera.take_photo(NEW_TRIAL_DIR)
    full_trial_file_name = os.path.join(NEW_TRIAL_DIR, new_trial_file_name)
    new_trial_features = features.get_features_for_image(full_trial_file_name)
    labels = classifier.predict(new_trial_features)
    if labels[0] == 0:
       shutil.move(full_trial_file_name,
                   os.path.join(NEGATIVE_TRIAL_DIR, new_trial_file_name))
    else:
       shutil.move(full_trial_file_name,
                   os.path.join(POSITIVE_TRIAL_DIR, new_trial_file_name))


if __name__ == '__main__':
    main()

