let tBody = $('#files-table').find('tbody');

let backup = [];
let editing = false;

function editElement(row) {
    if (!editing) {
        editing = true;
        let parent = $(row).parent();
        parent.parent().children().each(function () {
            if ($(this).attr('contenteditable')) {
                $(this).prop('contenteditable', true);
                backup.push($(this).text());
            }
        });
        parent.html('<a id="" href="#" onclick="saveEdit(this)">Save</a> / ' +
            '<a href="#" onclick="closeEdit(this,false)">Close</a>');
    }
}

function saveEdit(row) {
    let changes = [];
    let parent = $(row).parent();
    parent.parent().children().each(function () {
        if ($(this).attr('contenteditable')) {
            changes.push($(this).text())
        }
    });

    $.ajax({
        type : 'PUT',
        url : `/account/files/${backup}`,
        data : JSON.stringify(changes),
        dataType : 'json'
    })
    .done((res) => {
        $('#alerts').html(
            `<div class="alert alert-success text-center" role="alert">${res.old} to ${res.new} name changed.</div>`
        );
        backup = [];
        closeEdit(row, true);
    })
    .fail((erro) => {
       $('#alerts').html(
            `<div class="alert alert-warning text-center" role="alert">${erro.toString()}</div>`
        );
        closeEdit(row, false);
    });

}

function closeEdit(row, saved) {
    let parent = $(row).parent();
    parent.parent().children().each(function () {
        if ($(this).attr('contenteditable')) {
            $(this).prop('contenteditable', false);
            if (!saved) $(this).text(backup.pop());
        }
    });
    parent.html('<a href="#" onclick="editElement(this)">Edit</a>');
    editing = false;
}

function removeElements() {
    let files = [];
    let thIndex = $('#file-name').index();

    tBody.find('tr').each(function () {
        if ($(this).find('.check').prop('checked')) {
            $(this).find('td').each(function () {
                if ($(this).index() === thIndex) files.push($(this).text());
            });
            $(this).remove();
        }
    });

    $('#check-all').find('.check').prop('checked', false);

    $.ajax({
        type : 'DELETE',
        url : '/account/files',
        data : JSON.stringify(files),
        dataType : 'json'
    })
    .done((res) => {
        $('#alerts').html(
            `<div class="alert alert-success text-center" role="alert">${res.deleted} deleted.</div>`
        );
    })
    .fail((erro) => {
        $('#alerts').html(
            `<div class="alert alert-warning text-center" role="alert">${erro.toString()}</div>`
        );
    });
}

function checkAll(checkbox) {
    let master = $(checkbox).find('.check');
    master.prop('checked', !master.prop('checked'));
    $(".check").prop('checked', master.prop('checked'));
}

$(document).ready( function() {
    $('.sortable')
        .each(function () {
            let th = $(this),
                thIndex = th.index(),
                inverse = false;
            th.click(function () {
                tBody.find('td').filter(function () {
                    return $(this).index() === thIndex;
                }).sortElements(function (a, b) {
                    return $.text([a]) > $.text([b]) ?
                        inverse ? -1 : 1
                        : inverse ? 1 : -1;
                }, function () {
                    // parentNode is the element we want to move
                    return this.parentNode;
                });
                inverse = !inverse;
            });
        });

    $('#files-table td').click(function (e) {
        if (!$(e.target).is('a') && $(this).prop('contenteditable') !== 'true') {
            let checkbox = $(this).parent().find('.check');
            checkbox.prop('checked', !checkbox.prop('checked'));
        }
    });
});
