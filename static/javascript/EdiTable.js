let table = $('#files-table');
let tBody = table.find('tbody');

function editElement(row) {
    let parent = $(row).parent();
    parent.parent().children().each(function () {
        console.log($(this));
        if ($(this).attr('contenteditable')) {
            $(this).attr('contenteditable', true);
        }

    });
    parent.html('<a id="" href="#" onclick="saveEdit(this)">Save</a> / <a href="#" onclick="closeEdit(this)">Close</a>');


}

function saveEdit(row) {
    let parent = $(row).parent();
    let changes = [];
    parent.parent().children().each(function () {
        console.log($(this));
        if ($(this).attr('contenteditable')) {
            changes.push($(this).text())
        }
    });

    let changes_str = JSON.stringify(changes);
    console.log(changes);

    $.ajax({
        type : 'POST',
        url : '/account/change_file',
        data : changes_str,
        dataType : 'json'
    })
    .done(function() {
    });
    alert('saved');
    closeEdit(row);
}

function closeEdit(row) {
    let parent = $(row).parent();
    parent.parent().children().each(function () {
        console.log($(this));
        if ($(this).attr('contenteditable')) {
            $(this).attr('contenteditable', false);
        }

    });
    parent.html('<a href="#" onclick="editElement(this)">Edit</a>');
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
    let files_str = JSON.stringify(files);

    $.ajax({
        type : 'POST',
        url : '/account/delete_files',
        data : files_str,
        dataType : 'json'
    })
    .done(function() {
    });
}

$(document).ready( function() {
    $('#file-name, #addition-date')
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

    $('#check-all').click(function () {
        let master = $(this).find('.check');
        master.prop('checked', !master.prop('checked'));
        $(".check").prop('checked', master.prop('checked'));
    });

    $('#files-table td').click(function () {
        if ($(this).attr('contenteditable') !== 'true') {
            let checkbox = $(this).parent().find('.check');
            checkbox.prop('checked', !checkbox.prop('checked'));
        }
    });
});
