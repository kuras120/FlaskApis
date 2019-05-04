
function getStatus(taskID) {
  $.ajax({
    url: `/account/task_status/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.data.task_id}</td>
        <td>${res.data.task_status}</td>
        <td>${res.data.task_result}</td>
      </tr>`;
    $('#tasks').prepend(html);
    const taskStatus = res.data.task_status;
    if (taskStatus === 'finished' || taskStatus === 'failed') return false;
    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });
}

$(document).ready( function() {
    $('.btn').on('click', function () {
        $.ajax({
            url: '/account/queue_task',
            data: {type: $(this).data('type')},
            method: 'POST'
        })
            .done((res) => {
                getStatus(res.data.task_id)
            })
            .fail((err) => {
                console.log(err)
            });
    });
});