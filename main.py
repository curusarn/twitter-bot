#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from credentials import *
import os
import random
import sys
import time
import tweepy
import webbrowser
 

if __name__ == "__main__":

    #enter the corresponding information from your Twitter application:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    try:
        if not os.path.isfile("accessTokens"):
            raise Exception("UR mom is a hoe")

        with open("accessTokens", "r") as f:
            lines = f.readlines()
            auth.set_access_token(lines[0].strip(), lines[1].strip())

    except:
        # Open authorization URL in browser
        webbrowser.open(auth.get_authorization_url())

        # Ask user for verifier pin
        pin = input('Verification pin number from twitter.com: ').strip()

        ## Get access token

        ## Give user the access token
        #print('Access token:'.format(token))

        token = auth.get_access_token(verifier=pin)
        accessTokenFile = open("accessTokens","w")
        accessTokenFile.write(token[0]+'\n')
        accessTokenFile.write(token[1]+'\n')

    api = tweepy.API(auth)
     
    api.update_status("test: {0}".format(random.randint(1,1000)))
