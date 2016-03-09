#  -*- coding: utf-8 -*-

import os
import codecs
import random

# this is the path of the folder that will contain the tweet files
tweets_folder = os.path.join("D:", os.sep, "Documents", "PycharmProjects",
                             "easy_group_classifier", "text_files")

# checks if previous path exists, if not, it creates it
if not os.path.isdir(tweets_folder):
    os.makedirs(tweets_folder)

# the name of the file with clean tweets to scramble
filename = "technology"
tweets_file = os.path.join(tweets_folder, "%s.txt" % filename)
shuffled_file = os.path.join(tweets_folder, "%s_shuffled.txt" % filename)

tweet_list = []

with codecs.open(tweets_file, "rb", encoding="utf-8") as f:
    for line in f:
        tweet = line.strip()
        tweet_list.append(tweet)

random.shuffle(tweet_list)

with codecs.open(shuffled_file, "wb", encoding="utf-8") as f:
    for tweet in tweet_list:
        f.write("%s\n" % tweet)
