#  -*- coding: utf-8 -*-

import os

from tweepy import API, OAuthHandler

# keys and tokens obtained from personal twitter account
ckey = "xxxx"
csecret = "xxxx"
atoken = "xxxx"
asecret = "xxxx"

# this is the path of the folder that will contain the tweet files
tweets_folder = os.path.join("D:", os.sep, "Documents", "PycharmProjects",
                             "easy_group_classifier", "text_files")

# checks if previous path exists, if not, it creates it
if not os.path.isdir(tweets_folder):
    os.makedirs(tweets_folder)

# which user to get tweets from:
user = "BBCTech"

# this is to give the name of the file in which the tweets will be saved.
# it will be inside the previously mentioned tweets_folder
tweets_file = os.path.join(tweets_folder, "%s.txt" % user)
clean_tweets_file = os.path.join(tweets_folder, "%s_tweets_clean.txt" % user)


# this function is a modification of the one created by "yanofsky"
def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this
    # method

    # authorize twitter, initialize tweepy
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed
    # count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    # outtweets = [[tweet.id_str, tweet.created_at,
    #               tweet.text.encode("utf-8")] for tweet in alltweets]

    outtweets = []

    for tweet in alltweets:
        # this is to avoid getting truncated tweets as a result
        # of being retweets that end up being longer than 140 chars
        if tweet.text.endswith("…".decode("utf-8")):
            try:
                outtweets.append(tweet._json["retweeted_status"][
                                 "text"].encode("utf-8"))
            except:
                pass
        # it seems that twitter used to use three dots instead of
        # the ellipsis before, so this is to account for that
        elif tweet.text.endswith("...".decode("utf-8")):
            try:
                outtweets.append(tweet._json["retweeted_status"][
                                 "text"].encode("utf-8"))
            except:
                pass
        # if the tweet is "normal" this happens
        else:
            outtweets.append(tweet.text.encode("utf-8"))

    # write the file
    with open(tweets_file, 'wb') as f:
        for tweet in outtweets:
            f.write("%s\n" % tweet)

    pass

get_all_tweets(user)
