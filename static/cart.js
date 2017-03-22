/**
 * Created by troviln on 16.03.17.
 */
$(document).ready(function() {




    var basket = function() {

        if (Cookies.getJSON('goods') != '') {
            var ur = '/api/goods/?';

            if (Cookies.getJSON('goods') !== undefined) {

                var carts = Cookies.getJSON('goods');

                var arr = carts.split('');


                for (var i = 0; i < arr.length; i++) {

                    ur = ur + '&id=' + arr[i];


                }

                console.log(ur);


            }


            $.getJSON(ur, function (jd) {


                var my = $('.cart');
                var myl = '';
                //$('.cart').empty();

                for (i = 0; i < jd.objects.length; i++) {
                    var name = JSON.stringify(jd.objects[i].name);
                    var id = JSON.stringify(jd.objects[i].id);
                    console.log("JSON Data: " + name);
                    myl += '<div class=product data-good-id=' + id + '><p>' + name + '</p><button type="button" class="btn" id="delete">delete</button></div>';
                }

                my.html(myl);

                $('.cart #delete').click(function () {
                    var id = $(this).parent().attr('data-good-id');
                    console.log(id);
                    if (Cookies.getJSON('goods') !== undefined) {

                        var arr = Cookies.getJSON('goods');

                        var regexp = new RegExp(id);

                        arr = arr.replace(regexp, '')


                    }
                    console.log(arr);


                    Cookies.set("goods", JSON.stringify(arr));

                    var goods = Cookies.get("goods", {secure: true});
                    console.log("cookie", goods);
                    basket();


                })


            })

        }
        else {
            $('.cart').empty();

        }
    };

    basket();


    //$('#delete').click(function () {
    //    //var id = $(this).parent().attr('data-good-id');
    //    console.log("sdada");
    //    //
    //    //if (Cookies.getJSON('goods') !== undefined) {
    //    //
    //    //    var arr = Cookies.getJSON('goods');
    //    //
    //    //    var regexp = new RegExp(id);
    //    //
    //    //    arr = arr.substr(arr.search(regexp));
    //    //
    //    //
    //    //
    //    //}
    //    //console.log(arr);
    //    //
    //    //
    //    //
    //    //Cookies.set("goods", JSON.stringify(arr));
    //    //
    //    //var goods = Cookies.get("goods", { secure: true });
    //    //console.log(goods);
    //    //
    //    //
    //    // basket();
    //
    //
    //});



});