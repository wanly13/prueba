"""
seguir tutorial
https://towardsdatascience.com/how-to-extract-data-from-the-twitter-api-using-python-b6fbd7129a33
"""

#Import the necessary methods from tweepy library
import tweepy
from datetime import datetime
import time
import os
import params
import json

#This is a basic listener that just prints received tweets to stdout.
class TweetListener(tweepy.StreamingClient):
    def __open_file(self):
        now=datetime.now()
        filename = params.folder_path + "tweets_" + now.strftime("%Y-%m-%d")+".json"
        ptrFile = open(filename, "a+")
        return ptrFile

    def on_data(self, data):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " :: tweet read" )
        ptrFile = self.__open_file() 
        data = json.loads(data) 
        ptrFile.write(json.dumps(data["data"]))
        ptrFile.write("\n")
        ptrFile.close()
        return True

    def on_error(self, status):
        print("--- ERROR " + status + " ----")
        if status == 420:
            print("--- Waiting 15 minutes ---")
            time.sleep(15*60) #waiting by 15 minutes

if __name__ == '__main__':
    listener = TweetListener(params.bearer_token)
    rule = tweepy.StreamRule(' '.join(params.tracklist))
    listener.add_rules(rule)
            
    while(True):
        try:
            listener.filter()
        except Exception as e:
            print("---- CONNECTION ERROR ----", e)
            pass