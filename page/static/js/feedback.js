$(document).ready(function() {
    addComment();
});

// adds comment to db and refreshes page without reloading
function addComment(){
    $('button#comment-button').on("click", function(event) {
        console.log("clicked")
        var ajax_url = $(this).attr('data-ajax-url');
        var commentText = $('#comment-text').val();
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment_text: commentText,
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this,
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
             if(json.success === 'success') {
                var logInMessage = $('<p class="log-in-message">Successfully added comment</p>');
                $(logInMessage).appendTo($(this).parent().parent().parent()).fadeOut(700, function(){
                  $(this).remove();
                });
                $('#comments-list').empty(); // Clear the existing comments
                $.each(json.comments.commentsList, function(index, i) {
                    $('#comments-list').append(`
                        <li>
                            <img src='/static/img/personIcon.png'  alt='PersonIcon'>
                            <p><strong>${i.user}</strong> - ${i.date}:</p>
                            <p>${i.comment}</p>
                        </li>
                    `);
                });
                $('#comment-text').val('');
             } else {
                alert("Error: " + json.error);
             }
        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
        alert( "Sorry, there was a problem!" );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        // alert( "The request is complete!" );
        });
    });
}

// required CSRF cookie property for AJAX to modifiy
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
