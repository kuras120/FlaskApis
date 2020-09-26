
function getStatus(taskID, task_name, file_name, refresh) {
    $.ajax({
        url: `/account/task_status/${taskID}`,
        method: 'GET'
    })
    .done((res) => {
        if (refresh) {
            $('#tasks').find('.task-id').each(function () {
                if (res.data.task_id === $(this).text()) {
                    $(this).parent().replaceWith(`
                <tr>
                    <td class="task-id" style="display: none">${res.data.task_id}</td>
                    <td>${task_name} - ${file_name}</td>
                    <td>${res.data.task_status}</td>
                    <td>${res.data.task_result}</td>
                </tr>`)
                }
            });
        }
        else {
            const html = `
                <tr>
                    <td class="task-id" style="display: none">${res.data.task_id}</td>
                    <td>${task_name} - ${file_name}</td>
                    <td>${res.data.task_status}</td>
                    <td>${res.data.task_result}</td>
                </tr>`;
            $('#tasks').prepend(html);
        }

        let taskStatus = res.data.task_status;
        if (taskStatus === 'finished' || taskStatus === 'failed') return false;
        setTimeout(function() {
            getStatus(res.data.task_id, task_name, file_name, true);
        }, 1000);
    })
    .fail((err) => {
        console.log(err)
    });
}

function queue() {
    $.ajax({
    url: '/account/queue_task',
    data: {
        alg_path: $('#alg-path').val(),
        file_path: $('#file-path').val(),
        file_repr: $('#file-repr').val()
    },
    method: 'POST'
    })
    .done((res) => {
        getStatus(res.data.task_id, res.data.task_name, res.data.file_name, false)
    })
    .fail((err) => {
        console.log(err)
    });
}

$(document).ready(function () {
    if (window.location.pathname === '/account/') {
        $.ajax({
            url: '/account/tasks',
            method: 'GET'
        })
        .done((res) => {
            console.log(res);
            res.forEach(function (value) {
                console.log(value);
                getStatus(value.data.task_id, value.data.task_name, value.data.file_name, false)
            })
        })
        .fail((error) => {
           console.log(error)
        });
    }
});
