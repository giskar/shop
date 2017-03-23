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

            }


            $.getJSON(ur, function (jd) {


                var my = $('.cart');
                var my1 = $('#goods');
                var myl = '';
                var totalprice = 0;
                var order = '';
                //$('.cart').empty();

                for (i = 0; i < jd.objects.length; i++) {
                    var name = JSON.stringify(jd.objects[i].name);
                    var id = JSON.stringify(jd.objects[i].id);
                    var price = JSON.stringify(jd.objects[i].price);
                    order += id + name;


                    console.log("JSON Data: " + name);
                    myl += '<div class="good-container" product data-good-id=' + id + '><div class = "inline"> ' + name + ' </div><div class = "inline"> ' + price + '</div><button type="button" class="btn" id="delete">delete</button></div>';
                    totalprice += parseFloat(price)
                }

                myl += '<div class="good-container">'+ 'Total price: ' + totalprice + '</div>';
                myl += '<button type="button" class="btn btn-success" id="proceed">Proceed to purchase</button>'



                my.html(myl);
                my1.val(order);



                $('#proceed').click(function () {

                    var div = document.getElementById('box');

                    if(div.style.display == 'block') {

                        div.style.display = 'none';
                        //toggler.innerHTML = 'Открыть';
                    }
                    else {
                        div.style.display = 'block';
                        //toggler.innerHTML = 'Закрыть';
                    }




                });


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





});