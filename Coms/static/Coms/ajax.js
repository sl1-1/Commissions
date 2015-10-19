function buttonHandler(event) {
    var target = $('#' + event.target.id);
    var url = target.data()['url'];
    $('#' + target.data()['target']).load(url + ' .content')
}

function characterpopover(event) {
    var target = $('#' + event.target.id);
    $.get('/user/character/' + event.target.id + '/popover/', function (d) {
        target.popover({content: d, html: true, container: 'body', trigger: 'click'}).popover('show');
    });
}

function detailpopover(event) {
    var target = $('#' + event.target.id);
    console.log(target.data());
    $.get(target.data()['url'], function (d) {
        target.popover({content: d, html: true, container: 'body', trigger: 'click'}).popover('show');
    });
}




function register_events() {
    $('.action-btn').each(function (index, button) {
        button.onclick = buttonHandler;
    });

    $('.character-popover').each(function (index, button) {
        button.onclick = characterpopover;
    });
    $('.detail-popover').each(function (index, button) {
        button.onclick = detailpopover;
    });
    //noinspection JSUnusedGlobalSymbols
    $.fn.modal.Constructor.prototype.enforceFocus = function () { //This makes the modal not disappear when using select
    };
    $(".modal-action").on('click', function (event) {
        var modal = $('#detail-modal');
        $('#detail.content').removeData();
        buttonHandler(event);
        modal.modal('show');
        modal.data('url', $('#' + event.target.id).data()['url'])
    });
}

$(document).ajaxSuccess(function () {
    register_events();
});

$(document).ready(function () {
    $('.action-btn').each(function (index, button) {
        button.onclick = buttonHandler;
    });
    $(".modal-action").on('click', function (event) {
        var modal = $('#detail-modal');
        $('#detail.content').removeData();
        buttonHandler(event);
        modal.modal('show');
        modal.data('url', $('#' + event.target.id).data()['url'])
    });
});

