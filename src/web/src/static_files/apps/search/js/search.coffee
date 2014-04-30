
template_func = null;

$(document).ready ->
  template = $("#log_template").text()
  template_func = doT.template(template)
  $(".chosen").chosen({width:"100%"})

      #$("html, body").animate({scrollTop: $(document).height()}, 0)

  connection = new autobahn.Connection({
    url:"ws://localhost:6062/",
    realm: 'realm1'
  })

  connection.onopen = gotWebSocketConnection
  connection.open()
  null

node = document.getElementById("search_results")

clearSearchResults = () ->
  $("#search_results").empty()

displaySearchResults = (results, inc_counter=false) ->
  if inc_counter
    $("#hits").text +$("#hits").text() + 1

  for result in results
    $("#search_results").append(
          template_func(
            item: result
            getServerName: getServerNameFromID
            moment: moment
          )
        )

  child_count = document.querySelectorAll("#search_results > p").length

  if child_count > 500
    if results.length == 1
      node.removeChild(node.children[0])

  #$("html, body").animate({scrollTop: $(document).height()}, 0)


current_search_request = null;
current_search_subscription = null;
current_search_hash = null;

gotWebSocketConnection = (session) ->
  refresh_search_results = () ->
    query_string = $("#search_query").val()
    server_filter = $("#server_filter").val()
    stream_filter = $("#stream_filter").val()

    console.log query_string

    query = {query_string: query_string, server: server_filter, stream: stream_filter}

    if current_search_request != null
      # Cancel any previous request
      current_search_request.abort()

    $("#hits").text "..."
    $("#took").text "..."

    current_search_request = getSearchResults(query)
    current_search_request.done (data) ->
        clearSearchResults();
        $("#hits").text data.hits.total
        $("#took").text data.took

        displaySearchResults(data.hits.hits.reverse())

    session.call "logbook.update.subscribe", [query]
        .then (result) ->
            console.log result
            if current_search_subscription != null
                session.unsubscribe(current_search_subscription)
                session.call "logbook.update.unsubscribe", [current_search_hash]
            #current_search_subscription = result
            current_search_hash = result

            # We have a successful RPC result, we should now subscribe to the returned channel ID
            session.subscribe("logbook.live." + result, (args) -> displaySearchResults(args, true)).then(
              (sub) -> current_search_subscription = sub
              (err) -> console.log "Error subscribing"
            )

  refresh_search_results()
  $(".chosen").on('change', (evt, params) -> refresh_search_results())


getServerNameFromID = (id) ->
  window.serverNames[id]

getSearchResults = (query, size=100) ->
  $.get(Django.url("api:search"), $.extend({size: size}, query))