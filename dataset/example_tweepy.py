import tweepy
from tweepy import StreamingClient, StreamRule
import os
import json

 
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOqHggEAAAAAa25Ot%2Bb%2BgfkBXCouBJEcaEQWq%2Bk%3DE3SU4HwGqocG0ZKZncd7b8fxZA3DWb6xtxqhmpyJkFFm7Oi8by'
 
class TweetPrinterV2(tweepy.StreamingClient):
    
    def on_data(self, data):
        data = json.loads(data)
        print(json.dumps(data["data"]))
 
printer = TweetPrinterV2(bearer_token)
 
# add new rules    
rule = StreamRule(value="Python")
printer.add_rules(rule)
 
printer.filter()