
function getRequest(api, parameter, success) {
    var url = "http://127.0.0.1:5000/api/" + api;
    if (parameter != null && parameter != "") {
        url += "/" + parameter;
    }
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
            console.log("Unable to connect to " + url);
        }
    });
}

function renderFilters() {
    getRequest("getSearchFilters", null, function(filters) {
        var filtersDiv = $("#filters");
        filtersDiv.html("");
        for (var i = 0; i < filters.length; i++) {
            console.log("test");
            filtersDiv.append('<button type="input" class="btn btn-default filter-button">' + filters[i] +'</button><br>');
        }
    });
}

$(document).ready(function() {
    renderFilters();
});

$(document).on("click", "#add-filter-button", function() {
    var textbox = $("#add-filter-textbox");
    var filter = textbox.val().replace(" ", ""); // TODO support for spaces - use post request instead
    textbox.val("");
    if (filter != "") {
        getRequest("addSearchFilter", filter, function() {
            renderFilters();
        });
    }
});

$(document).on("click", ".filter-button", function() {
    getRequest("removeSearchFilter", $(this).text(), function() {
        renderFilters();
    });
});