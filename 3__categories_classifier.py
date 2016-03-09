#  -*- coding: utf-8 -*-

import codecs
import os
import pickle
import random

import nltk
from nltk.corpus import stopwords
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import word_tokenize

main_path = os.path.join("D:", os.sep, "Documents", "PycharmProjects",
                         "easy_group_classifier")
text_files = os.path.join(main_path, "text_files")
pickle_folder = os.path.join(main_path, "pickle_folder")

devtest_out = os.path.join(main_path, "devtest_output.txt")

politics_f = os.path.join(text_files, "politics.txt")
movies_f = os.path.join(text_files, "movies.txt")
tech_f = os.path.join(text_files, "technology.txt")

documents = []
all_words = []

with codecs.open(politics_f, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        documents.append((line, "politics"))
        all_words.extend(word_tokenize(line))

with codecs.open(movies_f, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        documents.append((line, "movies"))
        all_words.extend(word_tokenize(line))

with codecs.open(tech_f, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        documents.append((line, "technology"))
        all_words.extend(word_tokenize(line))

random.shuffle(documents)
print "length of documents: %s" % len(documents)


"""create a set with known stopwords in english"""
stop_words = set(stopwords.words("english"))


"""add part-of-speech (pos) to all the words in the 'all_words'"""
tagger = PerceptronTagger()
tagset = None
all_words_pos = nltk.tag._pos_tag(all_words, tagset, tagger)


"""select to filter for adjectives, adverbs and/or verbs"""
# J is adjective, R is adverb, and V is a verb
allowed_word_types = ["J", "V", "R"]


"""create a list of all words in 'all_words' that are not stop words, are not
   smaller than 3 characters, and are any of the allowed word types"""
all_words = []

# e.g. all_words_pos[0] = (u'The', 'DT')
#      all_words_pos[0][1] = u'DT'
#       all_words_pos[0][1][0] = 'D'
for w in all_words_pos:   # checking which kind of word we have
    if ((w[1][0] in allowed_word_types) and (len(w[0]) > 2) and
            (w not in stop_words)):
        all_words.append(w[0].lower())


"""get the frequency for each word in all_words"""
all_words = nltk.FreqDist(all_words)


"""create a list with the 3000 most common words in all_words"""
word_features = []
for word in all_words.most_common(3000):
    # print word
    word_features.append(word[0])

word_features_f = os.path.join(pickle_folder, "word_features.pickle")
# with open(word_features_f, "wb") as save_words:
#     pickle.dump(word_features, save_words)


def find_features(document_words):
    """find which words in a document are part of the 3000 most common words in
   all_words

   Or better said, for each document, check if it contains any of the 3000
   most common words."""
    # words = word_tokenize(document.decode('utf8', 'ignore'))
    words = document_words
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

feature_sets = [(find_features(rev), category)
                for (rev, category) in documents]

print "length of feature_sets: %s" % len(feature_sets)


"""define the training & testing sets (32000 for training, rest for testing)"""
training_set = feature_sets[:30000]
devtest_set = feature_sets[30000:32000]
testing_set = feature_sets[32000:]


"""default NLTK Naive Bayes CLassifier"""
classifier = nltk.NaiveBayesClassifier.train(training_set)

# save classifier for future use
# classifier_f = os.path.join(pickle_folder, "nltkNB.pickle")
# with open(classifier_f, "wb") as save_classifier:
#     pickle.dump(classifier, save_classifier)


"""Get info of errors using the devtest set"""
print nltk.classify.accuracy(classifier, devtest_set)

devtest_documents = documents[30000:32000]

errors = []
for (tweet, tag) in devtest_documents:
    guess = classifier.classify(find_features(tweet))
    tags_prob = classifier.prob_classify(find_features(tweet))
    politics_prob = tags_prob.prob("politics") * 100
    movies_prob = tags_prob.prob("movies") * 100
    tech_prob = tags_prob.prob("technology") * 100
    if guess != tag:
        errors.append((tag, guess, tweet, politics_prob, movies_prob,
                       tech_prob))

with codecs.open(devtest_out, "w", encoding="utf-8") as f:
    for (tag, guess, tweet, politics_prob, movies_prob,
         tech_prob) in sorted(errors):
        f.write("correct = %s\n" % tag)
        f.write("guess = %s\n" % guess)
        f.write("tweet = %s\n\n" % tweet)
        f.write("Likelihood: politics %.2f%%  movies %.2f%%  tech %.2f%%\n" %
                (politics_prob, movies_prob, tech_prob))
        f.write("----------------------------------------------------\n")
print "DONE!"

# classifier.show_most_informative_features(20)
exit()

org_accuracy_percent = nltk.classify.accuracy(classifier, testing_set) * 100
print "Original Naive Bayes algorithm accuracy: %s%%" % (org_accuracy_percent)
try:
    classifier.show_most_informative_features(200)
except UnicodeEncodeError:
    pass
