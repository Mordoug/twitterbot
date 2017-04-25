import twitter
import threading
from RateLimiter import *


class GiveawayManager:
    def __init__(self, api_in):
        self.api = api_in
        self.search_terms = []
        self.tweets = {}
        self.rateLimiter = RateLimiter(TwitterAuthType.USER_AUTH)

        threading.Timer(2*60*60, self.get_tweets).start()  # update tweets every 2 hours
        threading.Timer(900, self.giveaway_loop).start()

        self.ENABLED = False

    def giveaway_loop(self):
        '''
        pre: Pass in the tweets available
        Post: calls the enter_giveaway def 15 times
        Purpose: help ensure that the program doesnt go over the write limit
        '''
        for i in range(15):
            self.enter_giveaway(self.tweets)

    def enter_giveaway(self, status):
        '''
        Pre: Pass in an API object and a twitter.Status object
        Post: Retweet the tweet, favorite the tweet, and/or follow the user who posted the tweet as necessary
        Purpose: Enter a twitter giveaway based on instructions in the tweet
        '''
        RT = False  # Track if retweeting is necessary
        
        # Convert the twitter.Status object into a string and split it up to enable use of the status id and screen name
        status_string = status.__repr__()
        attributes = status_string.split(',')
        status_id = attributes[0].split('=')
        screen_name = attributes[1].split('=')
        content = attributes[3].split('=')
        text = content[1]
        is_retweet = text[:3]
        
        if is_retweet != "'RT" and is_retweet != '"RT':
        
            # Convert the twitter.Status string from unicode to ascii
            status_str = status_string.encode('ascii', 'ignore')
            status_str = status_str.lower()
            
            # Check and act upon entry requirements of the giveaway
            if ' rt ' in str(status_str):
                RT = True
            if ' rt' in str(status_str):
                RT = True
            if 'retweet' in str(status_str):
                RT = True
                
            if RT:
                self.rateLimiter.add_api_call(TwitterRateLimit.RETWEET, self.api.PostRetweet, status_id[1])
            if 'follow' in str(status_str):
                if 'notification' in str(status_str):
                    self.rateLimiter.add_api_call(TwitterRateLimit.FOLLOW, self.api.CreateFriendship, None,
                                                  screen_name[1], False)
                else:
                    self.rateLimiter.add_api_call(TwitterRateLimit.FOLLOW, self.api.CreateFriendship, None,
                                                  screen_name[1], False)
            if 'favorite' in str(status_str) or 'like' in str(status_str):
                # no limit?
                self.api.CreateFavorite(None, status_id[1])

    @staticmethod
    def get_query(search_term):
        search_filter = search_term.replace(" ", "%20")
        search_filter = search_filter.replace("#", "%23")
        # TODO fix dates
        return "l=en&q=Giveaway%20" + search_filter + "since%3A2017-03-22%20until%3A2017-03-23&src=typd&count=100"

    def get_tweets(self, search_term):
        self.tweets[search_term] = self.api.GetSearch(self.get_query(search_term))

        if self.ENABLED:
            for tweet in self.tweets[search_term]:
                try:
                    self.enter_giveaway(tweet)
                except twitter.TwitterError:
                    print("TwitterError")

    def update_tweets(self):
        self.tweets = {}
        for i in range(len(self.search_terms)):
            self.get_tweets(self.search_terms[i])

    def add_search_term(self, search_term):
        search_term = search_term.lower()
        if search_term not in self.search_terms:
            self.search_terms.append(search_term)
            self.get_tweets(search_term)

    def remove_search_term(self, search_term):
        if search_term in self.search_terms:
            self.search_terms.remove(search_term)
            self.tweets[search_term] = None

