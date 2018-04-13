#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import argparse
import configparser
import os
import random
import sys
import time
import tweepy
import webbrowser
 
def getKeysPath(config, key_type):
    path = config.get("keys", key_type)
    return os.path.expanduser(path)


def readKeys(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
            return (lines[0].strip(), lines[1].strip())
    return None
    
            
def writeKeys(path, key, secret):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if os.path.isdir(dirname):
        with open(path, "w") as f:
            f.write(key+'\n')
            f.write(secret+'\n')
        return True
    raise Exception("Could not create file <{0}>".format(path))


def main():
    config_path="./twitter-bot.ini"

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store", default=None,
                        help="Path to config (default <{0}>)"
                             .format(config_path))
    parser.add_argument("-r", "--retweet", action="store", default=None,
                        help="Retweet last N tweets from specified USER")
    parser.add_argument("-n", "--number", action="store", type=int, default=1,
                        help="Number of tweets (used by various options)") 
    parser.add_argument("-t", "--test",
                        help="Tweet N test tweets")

    args = parser.parse_args()
    if args.config:
        if not os.path.isfile(args.config):
            print("<{0}> in not a regular file - exiting!")
            parser.print_help()
            sys.exit(1)
        config_path = args.config

    config = configparser.ConfigParser()
    config.read(config_path)
    
    ###############
    # Consumer keys

    consumer_keys_path = getKeysPath(config, "consumer")

    consumer_keys = readKeys(consumer_keys_path)
    if consumer_keys:
        consumer_key, consumer_secret = consumer_keys
    else:
        consumer_key = input('consumer_key:').strip()
        consumer_secret = input('consumer_secret:').strip()
        writeKeys(consumer_keys_path, consumer_key, consumer_secret)

    #enter the corresponding information from your Twitter application:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    #############
    # Access keys

    access_keys_path = getKeysPath(config, "access")

    access_keys = readKeys(access_keys_path)
    if access_keys:
        auth.set_access_token(access_keys[0], access_keys[1])
    else:
        # Open authorization URL in browser
        webbrowser.open(auth.get_authorization_url())

        # Ask user for verifier pin
        pin = input('Verification pin number from twitter.com: ').strip()

        ## Get access token
        token = auth.get_access_token(verifier=pin)
        writeKeys(access_keys_path, token[0], token[1])

    api = tweepy.API(auth)
     
    ###########
    # AUTH done

    if args.test:
        for i in range(0, args.number):
            api.update_status("test: {0}".format(random.randint(1,1000)))

    if args.retweet:
        try:
            for x, status in enumerate(api.user_timeline(args.retweet)):
                if x >= args.number:
                    break
                print(x)
                api.retweet(status.id)
        except TweepError as e:
            print("TweepError while retweeting - <{0}>".format(e))
            pass


if __name__ == "__main__":
    main()

