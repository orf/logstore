
template_func = null;

$(document).ready ->
  query = $("#search_query").val()
  template = $("#log_template").text()
  template_func = doT.template(template)

  getSearchResults(query)
    .done (data) ->
      $("#hits").text data.hits.total
      $("#took").text data.took

      displaySearchResults(data.hits.hits.reverse())

      #$("html, body").animate({scrollTop: $(document).height()}, 0)

  ab.connect("ws://localhost:6062",
    gotWebSocketConnection(query),
    (code, reason) -> console.log "Error connecting to WebSockets: " + reason
  )

  null

node = document.getElementById("search_results")

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


gotWebSocketConnection = (query) ->
  (session) ->
    session.call "logbook/update#subscribe", query
      .then (result) ->
        # We have a successful RPC result, we should now subscribe to the returned channel ID
        session.subscribe("logbook/live/" + result
                          (uri, event) -> displaySearchResults([event], true)
                          (error, desc) -> console.log "Error: " + error + " Desc: " + desc)


getServerNameFromID = (id) ->
  window.serverNames[id]


getSearchResults = (query, size=100) ->
  $.get(Django.url("api:search"), {query: query, size: size})