

$(document).ready () ->
  $("#refresh_button").on "click", (ev) ->
    $.get(Django.url("api:random_log_message"),
      {format_id: $(this).attr("data-formatid")},
      (response) -> $("#id_input").val response
    )