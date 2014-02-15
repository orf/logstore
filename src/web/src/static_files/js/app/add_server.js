
$(document).ready(function(){
    $("#add_server_form").submit(function(event){
        event.preventDefault();
        var token_url = Django.url("api:create_install_token");

        $.post(token_url, $("#add_server_form").serialize(), function(data){
            var token = data.token;
            var url = data.url;
            $("#command_row").removeClass("hide");
            $("#add_server_form").hide();
            $("#install_command").val("curl " + url + " | bash");

            var spinner_place = document.getElementById('spinner_location');
            var spinner = new Spinner().spin(spinner_place);

            window.connectWebSocket(
                function(session){
                    session.subscribe("logbook/live/install/" + token, function(uri, event){
                        spinner.stop();
                        window.location.href = Django.url("servers:view", event.id);
                    });
                }
            );
        });
    })
});