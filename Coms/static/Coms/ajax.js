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

$(document).on('submit', '#statusform', function (ev) {
    var frm = $('#statusform');
    var formData = new FormData(frm[0]);
    $.ajax({
        processData: false,
        type: frm.attr('method'),
        url: frm.attr('action'),
        contentType: false,
        data: formData,
        success: function (data) {
            console.log(data);
            if (data == "Success") {
                $('.detail-popover').each(function () {
                    $(this).popover('destroy');
                });
                var load_url = $('#detail_id').val();
                 $('#detail-content').load(load_url + ' .content')
            }
            else {
                $(".popover-content").html(data)
            }
        }
    });
    ev.preventDefault();
});


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
    $('.lock-button').each(function (index, button) {
        button.onclick = function (event){
            var target = $('#' + event.target.id);
            var id = target.data()['id'];
            $.get('/admin/details/'+id+'/lock/').done(function (){ $('#commissiontable').DataTable().ajax.reload(); });
        };
    });
}

$(document).ajaxSuccess(function () { register_events(); });

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
    $('.datatable').dataTable();
        $('#detail-modal').on('hidden.bs.modal', function (event) {
        console.log(event);
        $('#commissiontable').DataTable().ajax.reload();
        $('.popover').each(function () {
            $(this).popover('hide');
        })
    });
});

