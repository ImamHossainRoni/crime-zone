(function ($) {
    $(document).ready(function () {
        // User login 
        $("#login-btn").on('click', function () {
            // console.log("Submit")

            $.ajax({
                url: '/api/login/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    // "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
                    "Content-Type": 'application/json'
                },
                data: JSON.stringify({
                    username: $("input[name = 'username']").val(),
                    password: $("input[name = 'password']").val(),

                })

            }).then(function (res) {
                if (res.success) {
                    window.location.href = '/home'

                }
                else {
                    window.alert("Username or Password not matched !")
                }
            });
            // location.reload();


        });

// User login end

// User registration
        $("#signupbutton").on('click', function () {
            $.ajax({
                url: '/api/create-user/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    "Content-Type": 'application/json'
                },
                data: JSON.stringify({
                    username: $("input[name = 'email']").val(),
                    first_name: $("input[name = 'first_name']").val(),
                    last_name: $("input[name = 'last_name']").val(),
                    password: $("input[name = 'password1']").val(),
                    confirm_password: $("input[name = 'password2']").val(),

                })

            }).then(function (res) {
                // console.log(res);
            });
            //location.reload();
        });
// User registration End      
        $("#logout-btn").on('click', function () {
            $.ajax({
                url: '/api/logout/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    "Content-Type": 'application/json'
                },


            }).then(function (res) {
                console.log("done");
                window.location.href = '/'
            });

        });

        var uploadImageString = "";
        function readFile() {
            if (this.files && this.files[0]) {
                var FR = new FileReader();

                FR.addEventListener("load", function (e) {
                    uploadImageString = e.target.result
                });
                FR.readAsDataURL(this.files[0]);
            }

        }
        document.getElementById('postimage').addEventListener('change', readFile);
        console.log(uploadImageString);

        // insert post
        $("#post").on('click', function () {
            $.ajax({
                url: '/api/post/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    "Content-Type": 'application/json'
                },
                processData: false,
                data: JSON.stringify({
                    title: $("textarea[name = 'title']").val(),
                    images: uploadImageString
                })

            }).then(function (res) {
                // console.log(res);
                console.log("Done");
            });
        });
        // insert post end


    })
})(jQuery);

