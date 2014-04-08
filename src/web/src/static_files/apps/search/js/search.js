// Generated by CoffeeScript 1.7.1
(function() {
  var clearSearchResults, current_search_request, displaySearchResults, getSearchResults, getServerNameFromID, gotWebSocketConnection, node, template_func;

  template_func = null;

  $(document).ready(function() {
    var connection, template;
    template = $("#log_template").text();
    template_func = doT.template(template);
    $(".chosen").chosen();
    connection = new autobahn.Connection({
      url: "ws://localhost:6062/",
      realm: 'realm1'
    });
    connection.onopen = gotWebSocketConnection;
    connection.open();
    return null;
  });

  node = document.getElementById("search_results");

  clearSearchResults = function() {
    return $("#search_results").empty();
  };

  displaySearchResults = function(results, inc_counter) {
    var child_count, result, _i, _len;
    if (inc_counter == null) {
      inc_counter = false;
    }
    if (inc_counter) {
      $("#hits").text(+$("#hits").text() + 1);
    }
    for (_i = 0, _len = results.length; _i < _len; _i++) {
      result = results[_i];
      $("#search_results").append(template_func({
        item: result,
        getServerName: getServerNameFromID,
        moment: moment
      }));
    }
    child_count = document.querySelectorAll("#search_results > p").length;
    if (child_count > 500) {
      if (results.length === 1) {
        return node.removeChild(node.children[0]);
      }
    }
  };

  current_search_request = null;

  gotWebSocketConnection = function(session) {
    var refresh_search_results;
    refresh_search_results = function() {
      var query, query_string, server_filter, stream_filter;
      query_string = $("#search_query").val();
      server_filter = $("#server_filter").val();
      stream_filter = $("#stream_filter").val();
      console.log(query_string);
      query = {
        query_string: query_string,
        server: server_filter,
        stream: stream_filter
      };
      if (current_search_request !== null) {
        current_search_request.abort();
      }
      $("#hits").text("...");
      $("#took").text("...");
      current_search_request = getSearchResults(query);
      current_search_request.done(function(data) {
        clearSearchResults();
        $("#hits").text(data.hits.total);
        $("#took").text(data.took);
        return displaySearchResults(data.hits.hits.reverse());
      });
      return session.call("logbook.update.subscribe", [query]).then(function(result) {
        console.log(result);
        return session.subscribe("logbook.live." + result, function(args) {
          return displaySearchResults([args], true);
        });
      });
    };
    refresh_search_results();
    return $(".chosen").on('change', function(evt, params) {
      return refresh_search_results();
    });
  };

  getServerNameFromID = function(id) {
    return window.serverNames[id];
  };

  getSearchResults = function(query, size) {
    if (size == null) {
      size = 100;
    }
    return $.get(Django.url("api:search"), $.extend({
      size: size
    }, query));
  };

}).call(this);

//# sourceMappingURL=search.map
