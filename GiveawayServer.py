from GiveawayManager import *
from flask import Flask, render_template, jsonify
app = Flask(__name__)


from requests_oauthlib import OAuth1Session
import webbrowser

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'


def startup():
    key = raw_input('Enter your consumer key: ')
    secret = raw_input('Enter your consumer secret: ')
    consumer_key, consumer_secret, access_token_key, access_token_secret = get_access_token(key, secret)
    api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
    return api


# THIS FUNCTION BELONGS TO THE PYTON-TWITTER-LIBRARY  I CHANGED THE FUNCTION TO RETURN A TOUPLE WITH THE INFO
# https://github.com/bear/python-twitter/blob/master/get_access_token.py
def get_access_token(consumer_key, consumer_secret):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')

    print('\nRequesting temp token from Twitter...\n')

    try:
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    print('I will try to start a browser to visit the following Twitter page '
          'if a browser will not start, copy the URL to your browser '
          'and retrieve the pincode to be used '
          'in the next step to obtaining an Authentication Token: \n'
          '\n\t{0}'.format(url))

    webbrowser.open(url)
    pincode = raw_input('\nEnter your pincode? ')

    print('\nGenerating and signing request for an access token...\n')

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=pincode)
    try:
        resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    print('''Your tokens/keys are as follows:
        consumer_key         = {ck}
        consumer_secret      = {cs}
        access_token_key     = {atk}
        access_token_secret  = {ats}'''.format(
            ck=consumer_key,
            cs=consumer_secret,
            atk=resp.get('oauth_token'),
            ats=resp.get('oauth_token_secret')))
    return consumer_key, consumer_secret, resp.get('oauth_token'), resp.get('oauth_token_secret')

giveaway_manager = GiveawayManager(startup())

@app.route("/")
def giveaway_page():
    return render_template("giveaways.html")


# TODO add error messages for api routes

@app.route("/api/getSearchFilters", methods=["GET"])
def get_search_filters():
    response = {"error": None, "data": None}

    response["data"] = giveaway_manager.search_terms
    return jsonify(response)


@app.route("/api/addSearchFilter/<search_filter>", methods=["GET"])
def add_search_filter(search_filter=None):
    response = {"error": None, "data": True}

    giveaway_manager.add_search_term(search_filter)
    return jsonify(response)


@app.route("/api/removeSearchFilter/<search_filter>", methods=["GET"])
def remove_search_filter(search_filter=None):
    response = {"error": None, "data": True}

    giveaway_manager.remove_search_term(search_filter)
    return jsonify(response)


@app.route("/api/getTweets/<search_filter>", methods=["GET"])
def get_tweets(search_filter=None):
    response = {"error": None, "data": None}

    response["data"] = giveaway_manager.tweets[search_filter]
    return jsonify(response)

if __name__ == "__main__":
    app.run(threaded=True)
