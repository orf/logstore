

$(document).ready ->
  query = $("#search_query").val()
  template = $("#log_template").text()
  template_func = doT.template(template)

  getSearchResults(query)
    .done (data) ->
      $("#hits").text data.hits.total
      $("#took").text data.took

      $("#search_results").append(
        template_func(
          messages: data.hits.hits.reverse()
          getServerName: getServerNameFromID
          moment: moment
        )
      )

      $("html, body").animate({scrollTop: $(document).height()}, 1000)


  null


getServerNameFromID = (id) ->
  console.log id
  window.serverNames[id]


getSearchResults = (query, size=100) ->
  $.get(Django.url("api:search"), {query: query, size: size})