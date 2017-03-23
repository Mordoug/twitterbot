
function getTweets(filter, success) {
    var url = "http://127.0.0.1:5000/api/tweets/" + filter;
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'get',
        success: function(response) {
            if (response.error == null) {
                success(response.data);
            } else {
                console.log(error);
            }
        },
        failure: function() {
            console.log("Unable to get tweets");
        }
    });
}

$(document).ready(function() {
    getTweets("gaming", function(tweets) {
        for (var i = 0; i < tweets.length; i++) {
            console.log(tweets[i]);
        }
    });
});