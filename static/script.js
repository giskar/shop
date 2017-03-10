/**
 * Created by troviln
 */
$(document).ready(function() {


    var good_id = $('.good-container').attr('data-good-id');
    var user_id = $('.good-container').attr('data-user-id');


    var post = function() {
           $.getJSON('/api/reviews/?goods='+good_id, function(jd) {

              $('.review-block').empty();

              for (i = 0; i < jd.objects.length; i++) {
                var data = JSON.stringify(jd.objects[i].review);
                console.log( "JSON Data: " + data);
                  $('.review-block').append('<p>'+data+'</p>');
              }




           })

    };

    $('.actions').click(function () {
        Cookies.set("username", $("input#username").val());
        Cookies.set("password", $("input#password").val());
        var username = Cookies.get("username", { secure: true });
        var password = Cookies.get("password", { secure: true });

    });

    $('#button1').click(function () {

        var goods =  good_id;
        var review = $('#review1').val();
        var author = user_id;
         console.log( author);
        if (author == ''){
            console.log( "author none");

        }

        else {


        $.ajax({
            url: 'http://127.0.0.1:5000/api/reviews/',
            headers: {
                "Authorization": "Basic " + btoa(Cookies.get("username") + ":" + Cookies.get("password"))
              },
            data: JSON.stringify({"goods": goods, "review": review, "author": author}),
            type: 'POST',
            contentType: 'application/json',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        }); }

        post()
    });



    $(window).load(function() {

        if (good_id !== undefined){
            post();
        }

    });

});


