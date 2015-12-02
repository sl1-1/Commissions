function setContact() {
    $('.selected').each(function () {
        $(this).val("False")
    });
    var formid = $('#PC').val();
    $('#id_contact_set-' + formid + '-primary').val(true);
}

function getOption() {
    var forms = $("#id_contact_set-TOTAL_FORMS").val();
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

