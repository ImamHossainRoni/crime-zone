
(function ($) {
    $(document).ready(function () {

        $.ajax({
            url:'/api/user/',
            method: 'GET',
            headers: {
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
                "Content-Type": 'application/json'
            },

        }).then(function(res){
            console.log(res)
        });

        // User login 
        $("#login-btn").on('click', function(){
            console.log("Submit")
        $.ajax({
            url:'/api/login/',
            method: 'POST',
            headers: {
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
                "Content-Type": 'application/json'
            },
            data: JSON.stringify({
                username: $("input[name = 'username']").val(),
                password: $("input[name = 'password']").val(),
              
            })

        }).then(function(res){
            if(res.success) {
                window.location.href = '/lol'
            }
        });
        // location.reload();
      });

// User login end

// User registration
    $("#signupbutton").on('click', function(){ 
    $.ajax({
        url:'/api/create-user/',
        method: 'POST',
        headers: {
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
            "Content-Type": 'application/json'
        },
        data: JSON.stringify({
            username: $("input[name = 'email']").val(),
            first_name: $("input[name = 'first_name']").val(),
            last_name: $("input[name = 'last_name']").val(),
            password: $("input[name = 'password1']").val(),
            confirm_password: $("input[name = 'password2']").val(),
          
        })

    }).then(function(res){
        // console.log(res);
    });
    location.reload();
  });
// User registration End



})
})(jQuery);