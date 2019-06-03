let tBody = $('#files-table').find('tbody');

let backup = [];
let editing = false;

function getElements() {
    $.ajax({
        type : 'GET',
        url : `/account/files`,
    })
    .done(function (data) {
        data.forEach(function (index, value) {
            tBody.append(
                `<tr>
                    <td>
                        <div class="custom-control custom-checkbox">
                            <input type="checkbox" class="custom-control-input check" id="custom-check-${index}">
                            <label class="custom-control-label" for="custom-check-${index}">${index}</label>
                        </div>
                    </td>
                    <td datatype="String" contenteditable="false">${value.name}</td>
                    <td datatype="Date-time">${value.added_on}</td>
                    <td><a href="#" onclick="editElement(this)">Edit</a></td>
                </tr>`
            );
        });
    })
    .fail(function (error) {
        if (error.status === 401) {
            window.location.href = error.responseJSON.redirect;
            return;
        }
        $('#alerts').html(
            `<div class="alert alert-warning text-center" style="display: none;" role="alert">${error.responseJSON.error}</div>`
        ).children().first().slideDown('fast');
    });
}

function addElement(input, home_catalog) {
    let formData = new FormData();
    formData.append('file', $(input)[0].files[0]);
    $.ajax({
        type : 'POST',
        url : `/account/files`,
        data : formData,
        dataType : 'json',
        cache:false,
        processData:false,
        contentType:false
    })
    .done(function (data) {
        let length = tBody.children().length + 1;
        tBody.append(
            `<tr>
                <td>
                    <div class="custom-control custom-checkbox">
                        <input type="checkbox" class="custom-control-input check" id="custom-check-${length}">
                        <label class="custom-control-label" for="custom-check-${length}">${length}</label>
                    </div>
                </td>
                <td datatype="String" contenteditable="false">${data.name}</td>
                <td datatype="Date-time">${data.added_on}</td>
                <td><a href="#" onclick="editElement(this)">Edit</a></td>
            </tr>`
        );
        $('#file-path').append(
            `<option value=Project/Server/DATA/${home_catalog}/${data.name}>${data.name}</option>`
        );
        $('#alerts').html(
            `<div class="alert alert-success text-center" style="display: none;" role="alert">${data.name} added.</div>`
        ).children().first().slideDown('fast');
    })
    .fail(function (error) {
        if (error.status === 401) {
            window.location.href = error.responseJSON.redirect;
            return;
        }
        $('#alerts').html(
            `<div class="alert alert-warning text-center" style="display: none;" role="alert">${error.responseJSON.error}</div>`
        ).children().first().slideDown('fast');
    });

    $(input).val('');
}

function editElement(row, home_catalog) {
    if (!editing) {
        editing = true;
        let parent = $(row).parent();
        parent.parent().children().each(function () {
            if ($(this).attr('contenteditable')) {
                $(this).prop('contenteditable', true);
                backup.push($(this).text());
            }
        });
        parent.html(
            `<a id="" href="#" onclick="saveEdit(this, '${home_catalog}')">Save</a> / <a href="#" onclick="closeEdit(this,false)">Close</a>`
        );
    }
}

function saveEdit(row, home_catalog) {
    let changes = [];
    let parent = $(row).parent();
    parent.parent().children().each(function () {
        if ($(this).attr('contenteditable')) {
            changes.push($(this).text())
        }
    });

    if (JSON.stringify(backup) === JSON.stringify(changes)) {
        closeEdit(row, false);
        return;
    }

    $.ajax({
        type : 'PUT',
        url : `/account/files/${backup}`,
        data : JSON.stringify(changes),
        dataType : 'json'
    })
    .done(function (data) {
        $(`#file-path option:contains('${backup[0]}')`).html(
            `<option value=Project/Server/DATA/${home_catalog}/${data.new_name}>${data.new_name}</option>`
        );

        $('#alerts').html(
            `<div class="alert alert-success text-center" style="display: none;" role="alert">
                ${data.old_name} to ${data.new_name} name changed.
             </div>`
        ).children().first().slideDown('fast');

        backup = [];
        closeEdit(row, true);

    })
    .fail(function (error) {
        if (error.status === 401) {
            window.location.href = error.responseJSON.redirect;
            return;
        }
        $('#alerts').html(
            `<div class="alert alert-warning text-center" style="display: none;" role="alert">${error.responseJSON.error}</div>`
        ).children().first().slideDown('fast');
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
    .done(function (data) {
        data.deleted_files.forEach(function (value) {
            $(`#file-path option:contains('${value}')`).remove();
        });

        $('#alerts').html(
            `<div class="alert alert-success text-center" style="display: none;" role="alert">
                ${data.deleted_files} deleted.
             </div>`
        ).children().first().slideDown('fast');
    })
    .fail(function (error) {
        if (error.status === 401) {
            window.location.href = error.responseJSON.redirect;
            return;
        }
        $('#alerts').html(
            `<div class="alert alert-warning text-center" style="display: none;" role="alert">${error.responseJSON.error}</div>`
        ).children().first().slideDown('fast');
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
