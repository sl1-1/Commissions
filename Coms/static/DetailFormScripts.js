function setContact() {
    $('.selected').each(function () {
        $(this).val("False")
    });
    var formid = $('#PC').val();
    $('#id_contact_set-' + formid + '-primary').val(true);
}

function getOption() {
    var obj = $("#id_contact_set-TOTAL_FORMS");
    var forms = obj.val();
    var select = $('#PC');
    $("select[id$=PC] > option").remove();
    select.empty();
    select.append(new Option('Email', 999, false, false));
    for (var i = 0; i < forms; i++) {
        var text = $('#id_contact_set-' + i + '-site :selected').text() + ': ' + $('#id_contact_set-' + i + '-username').val();
        if (!$("#id_contact_set-" + i + "-DELETE").prop('checked')) {
            if ($('#id_contact_set-' + i + '-site').val()) {
                select.append(new Option(text, i, false, false));
                if ($('#id_contact_set-' + i + '-primary').val().toLowerCase() == "true") {
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
        $('#submit').prop('disabled', true)
    }
    setContact()
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

function insertCharacter(event) {
    var character = event.target.id;
    var target = $('#' + (event.target.id));
    $.markItUp({replaceWith: '(!' + target.data()['name'] + ':' + character + ')'});
}

function addcharacterpopover(event) {
    console.log(event);
    var target = $('#' + this.id);
    $.get('/user/character/upload/ajax/', function (d) {
        target.popover({content: d, html: true, container: 'body', trigger: 'click', placement: 'top'}).popover('show');
    });
}

$(document).ready(function () {
    $("#characterlist").load("/user/character/ajax/");
    $('#addcharacterbutton').on('click', addcharacterpopover);
});

$(document).on('submit', '#characterupload', function (ev) {
    var frm = $('#characterupload');
    var formData = new FormData(frm[0]);
    var submitbutton = $("#charactersubmit");
    submitbutton.html("<i class=\"fa fa-spinner\"></i>");
    submitbutton.prop('disabled', true);
    $.ajax({
        processData: false,
        type: frm.attr('method'),
        url: frm.attr('action'),
        contentType: false,
        data: formData,
        success: function (data) {
            if (data == "Success") {
                $('#addcharacterbutton').popover('hide');
                $("#characterlist").load("/user/character/ajax/")
            }
            else {
                $(".popover-content").html(data)
            }
        }
    });
    ev.preventDefault();
});


$(document).ajaxSuccess(function () {
    $('.character').each(function (index, element) {
            element.onclick = insertCharacter;
        }
    );
});