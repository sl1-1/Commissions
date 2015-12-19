function characterpopover(event) {
    var target = $('#' + event.target.id);
    if (target.data()['bs.popover']) {
        target.popover('destroy');
        return;
    }
    $('.character-popover').each(function(index, button) {
        $(button).popover('destroy');
    });
    $.get('/character/' + event.target.id + '/popover/', function(d) {
        target.popover({
                content: d,
                html: true,
                container: 'body',
                trigger: 'click'
            })
            .popover('show');
    });
}

function detailpopover(event) {
    var target = $('#' + event.target.id);
    if (target.data()['bs.popover']) {
        target.popover('destroy');
        return;
    }
    $('.detail-popover').each(function(index, button) {
        $(button).popover('destroy');
    });
    var type = target.data()['type'];
    var url = '/api/commissions/' + target.data()['id'] + '/';
    $.getJSON(url, function(data) {
        var elm = document.createElement('select');
        elm.setAttribute('class', 'form-control');
        elm.setAttribute('name', type);
        var choices = data[type + '_choices'];
        for (var i = 0; i < choices.length; i++) {
            var choice = choices[i];
            var option = document.createElement('option');
            option.setAttribute('value', choice[0]);
            option.text = choice[1];
            elm.appendChild(option);
        }
        elm.options[data[type]].selected = true;
        var form = document.createElement('form');
        form.setAttribute('id', 'statusform');
        form.setAttribute('action', url);
        form.setAttribute('method', 'PATCH');
        form.appendChild(elm);
        var submit = document.createElement('input');
        submit.setAttribute('class', 'form-control');
        submit.setAttribute('type', 'submit');
        submit.setAttribute('value', 'Save');
        form.appendChild(submit);
        target.popover({
                content: form,
                html: true,
                container: 'body',
                trigger: 'click'
            })
            .popover('show');

    });
}


$(document).on('submit', '#statusform', function(ev) {
    var form = $(this);
    var url = form.attr('action');
    console.log();
    $.ajax({
        url: url,
        type: 'PATCH',
        data: form.serializeArray(),
        success: function(data) {
            reload_row(url);
            option_modal(data['id']);
            $('.detail-popover').each(function(index, button) {
                $(button).popover('destroy');
            });
        }
    });
    ev.preventDefault();
});

function option_modal(id) {
    var modal = $('#option-modal');
    if (typeof id != 'string') {
        id = $(this).data()['id'];
    }
    var url = modal.data()['src'] + id;
    if (modal.is(':visible') == false) {
        modal.empty();
    }
    modal.load(url + '/?format=form');
    $('#optionform').attr('data-url', url).attr('data-id', id);
    if (modal.is(':visible') == false) {
        modal.modal('show');
    }
}

function register_events() {
    $('.character-popover').each(function(index, button) {
        button.onclick = characterpopover;
    });
    $('.detail-popover').each(function(index, button) {
        button.onclick = detailpopover;
    });
    //noinspection JSUnusedGlobalSymbols
    $.fn.modal.Constructor.prototype.enforceFocus = function() {
        //This makes the modal not disappear when using select
    };
    $('.modal-action').each(function(index, button) {
        button.onclick = option_modal;
    });
}

$(document).ajaxSuccess(function() {
    register_events();
});

$(document).ready(function() {
    $('#option-modal').on('hidden.bs.modal', function() {
        $('.popover').each(function() {
            $(this).popover('hide');
        });
    });
    register_events();
});

//noinspection JSUnusedGlobalSymbols
function lockcom(event, state) {
    var id = $(event).data()['id'];
    $.ajax({
        url: '/api/commissions/' + id,
        type: 'PATCH',
        contentType: 'application/json',
        data: JSON.stringify({locked: state}),
        success: function(rvalue) {
            $('#commissiontable').DataTable().row('#' + id).data(rvalue).draw();
        }
    });
}

function setContact() {
    $('.selected').each(function() {
        $(this).val('False');
    });
    var formid = $('#PC').val();
    $('#id_form-' + formid + '-primary').val(true);
}

function getOption() {
    var forms = $('#id_form-TOTAL_FORMS').val();
    var select = $('#PC');
    $('select[id$=PC] > option').remove();
    select.empty();
    select.append(new Option('Email', 999, false, false));
    for (var i = 0; i < forms; i++) {
        var text = $('#id_form-' + i + '-site :selected')
                .text() + ': ' + $('#id_form-' + i + '-username').val();
        if (!$('#id_form-' + i + '-DELETE').prop('checked')) {
            if ($('#id_form-' + i + '-site').val()) {
                select.append(new Option(text, i, false, false));
                if ($('#id_form-' + i + '-primary')
                        .val().toLowerCase() == 'true') {
                    select.find('option:last').prop('selected', 'selected');
                }
            }
        }
    }
    var options = select.find('option');
    if (options.length) {
        $('#submit').prop('disabled', false);
    }
    else {
        $('#submit').prop('disabled', true);
    }
    setContact();
}

function paypalemail() {
    var email = $('#email').val();
    if ($('#paypalisemail').prop('checked')) {
        console.log(email);
        var paypal = $('#id_paypal');
        paypal.val(email);
        paypal.prop('readonly', true);
    }
    else {
        $('#id_paypal').prop('readonly', false);
    }

}

function disableForm() {
    $('input').attr('disabled', 'disabled');
    $('select').attr('disabled', 'disabled');
    $('textarea').attr('disabled', 'disabled');
}


function getColumnByClass(columns, className) {
    var indexes = [];
    $.each(columns, function(index, columnInfo) {
        if (columnInfo.className == className) {
            indexes.push(index);
        }
    });
    return indexes;
}

function getColumnByData(columns, data) {
    var indexes = [];
    $.each(columns, function(index, columnInfo) {
        console.log(columnInfo);
        if (columnInfo.data == data) {
            indexes.push(index);
        }
    });
    return indexes;
}

//noinspection JSUnusedLocalSymbols
function render_name(data, type, full) {
    if (full['details_submitted'] == false) {
        return data;
    }
    var btn = document.createElement('button');
    btn.className = 'btn btn-default modal-action btn-block';
    btn.setAttribute('data-id', full['id']);
    btn.appendChild(document.createTextNode(data));
    var wrapper = document.createElement('wrap');
    wrapper.appendChild(btn);
    return wrapper.innerHTML;
}

//noinspection JSUnusedLocalSymbols
function render_lock(data, type, full) {
    var btn = document.createElement('button');
    btn.className = 'btn btn-default btn-block lock-button';
    btn.setAttribute('id', 'lock-' + full['latest_detail']);
    btn.setAttribute('data-id', full['id']);
    btn.setAttribute('onclick', 'lockcom(this, ' + !data + ')');
    var icon = document.createElement('i');
    icon.setAttribute('style', 'pointer-events: none;');
    if (data == true) {
        icon.className = 'fa fa-lock';
    }
    else {
        icon.className = 'fa fa-unlock';
    }
    btn.appendChild(icon);
    var wrapper = document.createElement('wrap');
    wrapper.appendChild(btn);
    return wrapper.innerHTML;
}

//noinspection JSUnusedLocalSymbols
function render_queuelink(data, type, full) {
    var btn = document.createElement('a');
    btn.setAttribute('href', '/admin/queue/' + full['id'] + '/view');
    btn.appendChild(document.createTextNode(full['name']));
    var wrapper = document.createElement('wrap');
    wrapper.appendChild(btn);
    return wrapper.innerHTML;
}

function render_iconlink(data) {
    var elm = document.createElement('a');
    elm.setAttribute('href', data);
    elm.innerHTML = '<i class="fa fa-link"></i>';
    var wrapper = document.createElement('wrap');
    wrapper.appendChild(elm);
    return wrapper.innerHTML;
}

function render_iconbool(data) {
    if (data == true) {
        return '<i class="fa fa-check"></i>';
    }
    else {
        return '<i class="fa fa-close"></i>';
    }
}

function render_datetime(data) {
    var elm = document.createElement('time');
    elm.setAttribute('datetime', data);
    var text = document.createTextNode(moment(data).format('YYYY-MM-DD HH:MM'));
    elm.appendChild(text);
    var wrapper = document.createElement('wrap');
    wrapper.appendChild(elm);
    return wrapper.innerHTML;
}

function create_table(id, url, data) {
    var cols = data['cols'];
    var order;
    if (data['order']) {
        order = [getColumnByData(cols, data['order'])[0], 'asc'];
    }
    else {
        order = [];
    }
    console.log(getColumnByData(cols, order));
    $('#' + id)
        .dataTable({
            'columns': cols,
            'columnDefs': [
                {
                    'targets': getColumnByClass(cols, 'modallink'),
                    'data': 'id',
                    'render': render_name
                },
                {
                    'targets': getColumnByClass(cols, 'iconlink'),
                    'orderable': false,
                    'render': render_iconlink
                },
                {
                    'targets': getColumnByClass(cols, 'iconbool'),
                    'render': {
                        'display': render_iconbool
                    }
                },
                {
                    'targets': getColumnByClass(cols, 'queuelink'),
                    'render': render_queuelink
                },
                {
                    'targets': getColumnByClass(cols, 'iconlock'),
                    'render': {
                        'display': render_lock
                    }
                },
                {
                    'targets': getColumnByClass(cols, 'datetime'),
                    'render': {
                        'display': render_datetime
                    }
                }
            ],
            'dom': "<'row'<'col-sm-3'l><'col-sm-5 toolbar'><'col-sm-4'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'i><'col-sm-7'p>>",
            'sAjaxDataProp': '',
            'ajax': url,
            'rowId': 'id',
            'order': order,
            'responsive': true,
            'bAutoWidth': false
        });
}

function reload_row(url) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function(rvalue) {
            var id = rvalue['id'];
            $('.dataTable').DataTable().row('#' + id).data(rvalue).draw();
        }
    });
}

$(document).on('submit', '#optionform', function(ev) {
    var form = $(this);
    var data = form.serializeArray();
    var method;
    if (form.data()['id'] == '') {
        method = 'POST';
    }
    else {
        method = 'PUT';
    }
    $.ajax({
        url: form.data()['url'] + '?format=form',
        type: method,
        data: data,
        statusCode: {
            400: function(rvalue) {
                $('#option-modal').html(rvalue.responseText);
            }
        },
        success: function() {
            var modal = $('#option-modal');
            modal.modal('hide');
            if (form.data()['id'] == '') {
                $('#optiontable').DataTable().ajax.reload(null, false);
            }
            else {
                reload_row(form.data()['url']);
            }
        }
    });
    ev.preventDefault();
});


function new_option() {
    var modal = $('#option-modal');
    var id = $(this).data()['id'];
    var url = modal.data()['src'];
    modal.empty();
    modal.load(url + '?format=form');
    modal.modal('show');
}

function clear_input(input) {
    $('input[name=' + input + ']').val('');
}

//$('html').on('click', function (e) {
//    if (typeof $(e.target).data('original-title') == 'undefined') {
//        $('[data-original-title]').popover('destroy');
//    }
//});
