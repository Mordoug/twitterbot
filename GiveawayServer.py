from flask import Flask, render_template, jsonify
app = Flask(__name__)

tweets = {"gaming": ["tweet1", "tweet2", "tweet3"]}

@app.route("/")
def giveaway_page():
    return render_template("giveaways.html")


@app.route("/api/tweets/<tweet_filter>")
def get_tweets(tweet_filter=None):
    message = {"error": None, "data": None}

    if tweet_filter is None:
        message["error"] = "Filter not specified"
        return jsonify(message)

    if tweet_filter in tweets:
        message["data"] = tweets[tweet_filter]
        return jsonify(message)
    else:
        message["error"] = tweet_filter + " is not a valid filter"
        return jsonify(message)

if __name__ == "__main__":
    app.run()
