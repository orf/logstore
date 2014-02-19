

$(document).ready ->
  query = $("#search_query").val()
  template = $("#log_template").text()

  getSearchResults(query)
    .done (data) -> console.log data


  null


getSearchResults = (query, size=100) ->
  $.get(Django.url("api:search"), {query: query, size: size})