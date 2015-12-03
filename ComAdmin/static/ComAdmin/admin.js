function lockcom(event) {
    var target = $('#' + event.id);
    var id = target.data()['id'];
    $.get('/admin/details/' + id + '/lock/').done(function () {
        $('#commissiontable').DataTable().ajax.reload();
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

$(document).ready(function () {
    $('#detail-modal').on('hidden.bs.modal', function (event) {
        console.log(event);
        $('#commissiontable').DataTable().ajax.reload();
        $('.popover').each(function () {
            $(this).popover('hide');
        })
    });
    $('.datatable').dataTable();
});