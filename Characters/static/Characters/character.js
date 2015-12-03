function charmodal() {
    var modal = $('#char-modal');
    var content = $('#char-content');
    content.load('/character/ajax/');
    modal.modal('show');
}


function insertCharacter(event) {
    var character = event.id;
    var target = $('#' + (event.id));
    $('#id_details').focus();
    $.markItUp({replaceWith: '(!' + target.data()['name'] + ':' + character + ')'});
    var modal = $('#char-modal');
    modal.modal('hide');
}

function uploadChar() {
    var modal = $('#char-modal');
    var content = $('#char-content');
    content.load('/character/upload/ajax/');
}

function cancelChar() {
    var modal = $('#char-modal');
    var content = $('#char-content');
    content.load('/character/ajax/');
}

$(document).ready(function () {
    var markItUpHeader = $('.markItUpHeader');
    markItUpHeader.children("ul").append('<li class="markItUpSeparator">---------------</li>');
    markItUpHeader.children("ul").append('<li class="markItUpButton" id="charbutton"><i class="fa fa-users" style="cursor: pointer" title="Characters"></i></li>');
    var charbutton = $('#charbutton');
    charbutton.bind('click.markItUp', function (e) {
        e.preventDefault();
    });
    charbutton.click(charmodal)
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
                $('#char-content').load("/character/ajax/")
            }
            else {
                $('#char-content').html(data)
            }
        }
    });
    ev.preventDefault();
});