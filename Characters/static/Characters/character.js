function charmodal() {
    var modal = $('#char-modal');
    var content = $('#char-content');
    content.load('/character/ajax/', function () {
        $(".character").each(function (index, button) {
            button.onclick = insertCharacter(event)
        })
    });
    modal.modal('show');
}

function uploadChar() {
    var full = $(event.target).data()['full'];
    var modal = $('#char-modal');
    var content = $('#char-content');
    content.load('/character/upload/', function () {
        if (full == true) {
            $('#charactersubmit').data('full', true);
        }
        $('#addcharacter').click(function () {
            if (full == true) {
                modal.modal('hide');
            }
            else {
                charmodal()
            }
        })
    });
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

function registerEvents() {
    $(".character").each(function (index, button) {
        console.log(button);
        button.onclick = (
            function (event) {
                window.open('/character/' + event.target.id, '_self');
            }
        )
    })
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
                if(submitbutton.data()['full'] == true){
                    $('#characterlist').load('/character/ajax/ #characterlist');
                    $('#char-modal').modal('hide');
                }
                else{
                    $('#char-content').load("/character/ajax/")
                }
            }
            else {
                $('#char-content').html(data)
            }
        }
    });
    ev.preventDefault();
});
