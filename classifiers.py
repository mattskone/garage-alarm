from sklearn import cross_validation, svm


def get_trained_classifier(samples, labels):
    classifier = svm.SVC(kernel='linear')
    classifier.fit(samples, labels)

    return classifier

