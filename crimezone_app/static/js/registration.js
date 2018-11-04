
(function ($) {
    $(document).ready(function () {

        // User registration
      $("#signupbutton").on('click', function(e){
        e.preventDefault();
        $.ajax({
            url:'/api/create-user/',
            method: 'POST',
            headers: {
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
            },
            data:{
                username: $("input[name = 'username']").val(),
                first_name: $("input[name = 'first_name']").val(),
                last_name: $("input[name = 'last_name']").val()
              
            }

        }).then(function(res){
            console.log("Inserted");
        });
      });
 // User registration End


    })
})(jQuery);