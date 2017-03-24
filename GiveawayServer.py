from GiveawayManager import *
from flask import Flask, render_template, jsonify
app = Flask(__name__)

giveaway_manager = GiveawayManager()


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
    app.debug = True
    app.run(threaded=True)
