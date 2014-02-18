
$(document).ready(function(){
    var query = $("#search_query").val();
    var template = $("#log_template").text();

    $.get(Django.url("api:search"), {query: query, size: 100}, function(data){
        var output = Mustache.render(template,
            {
                messages:data.hits.hits.reverse(),
                date:function() {
                    return function(text, render) {
                        var d = new Date(render(text));
                        return d.getDate() + "/" + (d.getMonth() + 1) + "/" + d.getFullYear();
                    }
                },
                time:function() {
                    return function(text, render){
                        var d = new Date(render(text));
                        return d.toLocaleTimeString();
                    }
                }
            });
        $("#search_results").append($(output));
        $("#hits").text(data.hits.total);
        $("#took").text(data.took);
    });

    window.connectWebSocket(
        function(session){
            session.call("logbook/update#subscribe", query).then(
                function(result){
                    session.subscribe("logbook/live/" + result, function(uri, event){
                        $("#search_results").append(
                            $(Mustache.render(template, {messages:[{_source:{message:event.line}}]}))
                        );
                        var hits = $("#hits");
                        hits.text(parseInt(hits.text()) + 1)
                    })
                }
            );
        }
    );
});