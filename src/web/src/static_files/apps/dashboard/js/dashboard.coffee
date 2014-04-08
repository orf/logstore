
messages =
  global_message_rates: (0 for num in [0..29])
  event_rates: (0 for num in [0..29])
  processed_message: (0 for num in [0..29])


$(document).ready ->
  connection = new autobahn.Connection({
    url:"ws://localhost:6062/",
    realm: 'realm1'
  })

  connection.onopen = gotWebSocketConnection
  connection.open()



gotWebSocketConnection = (session) ->
  console.log "Subscribed"

  session.subscribe(
    "logbook.stat.got_log_line",
    (args) -> updateSpeedGraph("global_message_rates", args[0])
  )

  session.subscribe(
    "logbook.stat.got_event_hit",
    (args) -> updateSpeedGraph("event_rates", args[0])
  )

  session.subscribe(
    "logbook.stat.processed_message",
    (args) -> updateSpeedGraph("processed_message", args[0])
  )



updateSpeedGraph = (name, message_rate) ->
  messages[name].push(message_rate)

  if messages[name].length > 30
    messages[name] = messages[name].slice(1, 31)

  $("##{ name }_graph").sparkline(messages[name])
  $("##{ name }_text").text(message_rate)