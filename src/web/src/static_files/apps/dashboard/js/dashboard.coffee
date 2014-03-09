
global_message_rates = (0 for num in [0..29])

console.log(global_message_rates)
$(document).ready ->
  ab.connect("ws://localhost:6062",
                gotWebSocketConnection,
                (code, reason) -> console.log "Error connecting to WebSockets: " + reason
              )



gotWebSocketConnection = (session) ->
  console.log "Subscribed"
  session.subscribe(
    "logbook/stat/got_log_line"
    (uri, event) -> ($("#messages_per_sec").text(event); updateMessageSpeedGraph(event))
    (error, desc) -> console.log "Error: " + error + " Desc: " + desc
  )

updateMessageSpeedGraph = (message_rate) ->
  global_message_rates.push(message_rate)

  if global_message_rates.length > 30
    global_message_rates = global_message_rates.slice(1, 31)

  console.log(global_message_rates)

  $("#message_rate_graph").sparkline(global_message_rates)
