$(document).ready( function() {
    $('#like-button').click(function() {
        $.ajax("/add_like/").done(function (data) {
            $('#like-button').html(" " + data);
        });
    });
});
