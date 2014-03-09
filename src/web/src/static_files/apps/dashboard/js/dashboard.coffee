
messages =
  global_message_rates: (0 for num in [0..29])
  event_rates: (0 for num in [0..29])
  processed_message: (0 for num in [0..29])


$(document).ready ->
  ab.connect("ws://localhost:6062",
                gotWebSocketConnection,
                (code, reason) -> console.log "Error connecting to WebSockets: " + reason
              )



gotWebSocketConnection = (session) ->
  console.log "Subscribed"
  session.subscribe(
    "logbook/stat/got_log_line"
    (uri, event) -> updateSpeedGraph("global_message_rates", event)
    (error, desc) -> console.log "Error: " + error + " Desc: " + desc
  )
  session.subscribe(
    "logbook/stat/got_event_hit"
    (uri, event) -> updateSpeedGraph("event_rates", event)
    (error, desc) -> console.log "Error: " + error + " Desc: " + desc
  )
  session.subscribe(
    "logbook/stat/processed_message"
    (uri, event) -> updateSpeedGraph("processed_message", event)
    (error, desc) -> console.log "Error: " + error + " Desc: " + desc
  )

updateSpeedGraph = (name, message_rate) ->
  messages[name].push(message_rate)

  if messages[name].length > 30
    messages[name] = messages[name].slice(1, 31)

  $("##{ name }_graph").sparkline(messages[name])
  $("##{ name }_text").text(message_rate)