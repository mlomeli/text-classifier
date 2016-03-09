#  -*- coding: utf-8 -*-

import HTMLParser
import os
import re

from nltk import word_tokenize

html_parser = HTMLParser.HTMLParser()

# this is the path of the folder that will contain the tweet files
tweets_folder = os.path.join("D:", os.sep, "Documents", "PycharmProjects",
                             "easy_group_classifier", "text_files")

# checks if previous path exists, if not, it creates it
if not os.path.isdir(tweets_folder):
    os.makedirs(tweets_folder)

# the name of the file to clean
word = "BBCTech"

# this is name of the file that contains all the "unclean" tweets.
# it will be inside the previously mentioned tweets_folder
tweets_file = os.path.join(tweets_folder, "%s.txt" % word)
clean_tweets_file = os.path.join(tweets_folder, "%s_clean.txt" % word)

tweet_list = []

# read "unclean" tweets from file
with open(tweets_file, "rb") as f:
    for line in f:
        tweet_list.append(line.strip())


def remove_urls_n_bloat(text):
    """Remove any URL, mention and hashtag symbol included in the text."""

    # this removes URLs,  mentions and RT bloat
    new_text = " ".join(
        re.sub("(@[A-Za-z0-9_]+)|(\w+:\/\/\S+)|(^RT)|(:\s+)",
               " ", text).split())

    # this removes the hashtag symbols only from hashtaged words
    newer_text = re.sub("(#[A-Za-z]+[A-Za-z0-9]*)|(#[0-9]+[A-Za-z]+)",
                        lambda m: m.group(0)[1:], new_text)

    return newer_text


def remove_emoticons(text):
    """Remove emoticons, emoji and pictograph characters from the text."""

    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
                          u'\U0001F300-\U0001F64F'
                          u'\U0001F680-\U0001F6FF'
                          u'\u2600-\u26FF\u2700-\u27BF]+',
                          re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
                          u'\ud83c[\udf00-\udfff]|'
                          u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                          u'[\u2600-\u26FF\u2700-\u27BF])+',
                          re.UNICODE)
    unicode_text = text.decode("utf-8")
    new_text = myre.sub('', unicode_text).encode("utf-8")

    return new_text


def escape_HTML_chars(text):
    """Escape any HTML characters present in the text."""

    text = text.decode("utf-8")
    new_text = html_parser.unescape(text).encode("utf-8")

    return new_text


def separate_punctuation(text):
    """Separate punctuation marks in the text.
    e.g. "I have a question, what is your name?"
         --> "I have a question , what is your name ?"
    """
    text = text.decode("utf-8")
    word_tokens = word_tokenize(text, "english")
    new_text = " ".join(word_tokens).encode("utf-8")

    return new_text


def separate_joint_words(name):
    """Separate the remains of previously hashtaged words into
    base words.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()


clean_tweet_list = []

for tweet in tweet_list:
    tweet = remove_urls_n_bloat(tweet)
    tweet = remove_emoticons(tweet)
    tweet = escape_HTML_chars(tweet)
    tweet = separate_joint_words(tweet)
    tweet = separate_punctuation(tweet)
    clean_tweet_list.append(tweet)

# this is to get rid of repeated tweets
clean_tweet_list = list(set(clean_tweet_list))

# write the cleaned tweets to a file
with open(clean_tweets_file, "wb") as f:
    for tweet in clean_tweet_list:
        f.write("%s\n" % tweet)
