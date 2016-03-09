#  -*- coding: utf-8 -*-

import os
import pickle

from nltk.tokenize import word_tokenize

main_path = os.path.join("D:", os.sep, "Documents", "PycharmProjects",
                         "easy_group_classifier")
pickle_folder = os.path.join(main_path, "pickle_folder")


word_features_f = os.path.join(pickle_folder, "word_features.pickle")
with open(word_features_f, "rb") as save_words:
    word_features = pickle.load(save_words)


def find_features(document_words):
    """find which words in a document are part of the 3000 most common words in
   all_words

   Or better said, for each document, check if it contains any of the 3000
   most common words."""
    words = word_tokenize(document_words.decode('utf8', 'ignore'))
    # words = document_words
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

# default NLTK Naive Bayes CLassifier
classifier_f = os.path.join(pickle_folder, "nltkNB.pickle")
with open(classifier_f, "rb") as saved_classifier:
    classifier = pickle.load(saved_classifier)

text = ''

while not text == 'q':
    text = raw_input("Text to classify: ")
    if text == 'q':
        break
    predicted_tag = classifier.classify(find_features(text))
    tags_prob = classifier.prob_classify(find_features(text))
    politics_prob = tags_prob.prob("politics") * 100
    movies_prob = tags_prob.prob("movies") * 100
    tech_prob = tags_prob.prob("technology") * 100
    print ""
    print "The most likely category for this text is: %s\n" % predicted_tag
    print "Probabilty for the category being politics: %.2f%%" % politics_prob
    print "Probabilty for the category being movies: %.2f%%" % movies_prob
    print "Probabilty for the category being technology: %.2f%%\n" % tech_prob
