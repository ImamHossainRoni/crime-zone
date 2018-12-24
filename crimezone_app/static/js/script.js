(function ($) {
    $(document).ready(function () {
        // User login 
        $("#login-btn").on('click', function () {

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
                    window.location.href = res.success_url

                } else {
                    window.alert("Username or Password not matched !")
                }
            });
            // location.reload();


        });

// User login end

// var user_name =  $("input[name = 'email']").val(),
// var firstname =  $("input[name = 'first_name']").val(),
// var lastname = $("input[name = 'last_name']").val(),
// var pass1= $("input[name = 'password1']").val(),
// var pass2 = $("input[name = 'password2']").val()

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
                location.reload();
            });
        });
        // insert post end

        // Modal data show
        $('#postdetails').on('show.bs.modal', function (e) {
            var picUrl = ($(e.relatedTarget).data('photo'));
            var status = ($(e.relatedTarget).data('status'));
            if (picUrl) {
                $('#m-post-img').html('<img src="' + picUrl + '" alt="' + status + '"/>');
            }
            $('#m-post-title').html(status)
        });

        // Comment Part
        $(document).on('submit', '.comment-form', function (e) {
            e.preventDefault();
            var commentText = e.target.elements[0].value;
            var commentPostId = e.target.elements[1].value;
            $.ajax({
                url: '/api/comment/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    "Content-Type": 'application/json'
                },
                processData: false,
                data: JSON.stringify({
                    comment: commentText,
                    post: commentPostId
                })

            }).then(function (res) {
                location.reload();
            });
        });

        // Reply Part
        $(document).on('click', '.reply-submit-btn', function (e) {
            e.preventDefault();
            var replyText = e.target.parentElement.children[0].value;
            var commentId = e.target.parentElement.children[1].value;
            $.ajax({
                url: '/api/reply/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    "Content-Type": 'application/json'
                },
                processData: false,
                data: JSON.stringify({
                    reply: replyText,
                    comment: commentId
                })

            }).then(function (res) {
                location.reload();
            });
        });

        // Like part
        $(document).on("click", ".likebutton", function () {
            $.ajax({
                url: '/api/like/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    "Content-Type": 'application/json'
                },
                processData: false,
                data: JSON.stringify({
                    post: $(this).data('post')
                })

            }).then(function (res) {
                console.log(res)
                $('#like-count-' + res.post).html('(' + res.total_likes + ')');
                if (res.i_liked) {
                    $(".like-unlike-btn-text-" + res.post).html('Unstar')
                } else {
                    $(".like-unlike-btn-text-" + res.post).html('Star')
                }
            });
        });

        // User deactivate
        $(document).on('click', '.deactive-btn', function (e) {
            var user = this.dataset['user']
            var status = this.dataset['status']
            var vm = this;
            $.ajax({
                url: '/api/active-deactive/',
                method: 'POST',
                headers: {
                    "X-CSRFToken": localStorage.getItem('csrf_token'),
                    "Content-Type": 'application/json'
                },
                processData: false,
                data: JSON.stringify({
                    user: user
                })

            }).then(function (res) {
                $(vm).html(res.is_active === false ? 'Active' : 'Deactive')
            });
        })

    })
})(jQuery);

