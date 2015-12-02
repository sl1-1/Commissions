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