function Site() {
    // Send a toast notification.
    this.toast = function(message){
        Materialize.toast(message, 4000);
    }
    // Make a call to the api.
    this.api = function(action, data, callback){
        var baseURL = "";
        // var baseURL = "http://mwtn.uk/git/coder8/site/";
        $.post(
            baseURL + "api.py/" + action,
            data,
            callback
        );
    }
    // Turns an element filled with markdown into HTML
    this.markdown = function(id){
        var md = new showdown.Converter();
        var text = $(id).text();
        $(id).html(md.makeHtml(text));
    }
    this.route = function(path){
        document.querySelector('app-router').go(path);
    }
    this.notify = function(title, text, buttons){
        $('#notification').empty();
        var buttonDiv = $('<div/>')
            .attr('id', 'buttons')
        ;
        for (var i in buttons) {
            var button = buttons[i];
            buttonDiv.append(
                $('<a/>')
                    .addClass('waves-effect')
                    .addClass('waves-light')
                    .addClass('btn')
                    .addClass(button[1])
                    .text(button[0])
                    .click(button[2])
            );
        }
        $('#notification').append(
            $('<h2/>')
                .text(title),
            $('<p/>')
                .text(text),
            buttonDiv
        );
    }
    this.notify_toggle = function(){
        $('#notification')[0].toggle();
    }
}
var site = new Site()
