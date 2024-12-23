function showDiscountNotification() {
    console.log("hehe")
    // Cài đặt vị trí thông báo
    message = "Laptop Acer đang giảm giá sốc!"
    alertify.set('notifier', 'position', 'bottom-left');
    let duration = 0;


    // Tạo thông báo tùy chỉnh

    alertify.notify(`
        <div class="custom-alertify" style="width: 420px;height:130px;padding:5px;" >
            
            <img style="width: 100px;height:100px;"  src="https://res.cloudinary.com/dc4bgvfbj/image/upload/v1730446605/fresh_mart/dufkjrxyegjamdcxl13o.jpg" class="alertify-icon" />
            <div class="alertify-content">
                <div class="countdown-container">
                    <div class="countdown">
                        Còn
                        <p id="hours"></p>
                        <span>giờ</span>
                        <p id="minutes"></p>
                        <span>phút</span>
                        <p id="seconds"></p>
                        <span>giây</span>
                    </div>
                </div>
                <i class="fa-solid fa-bolt" style="color: #ffa53d;"></i>
                <strong>${message}</strong>
                <a style="margin-top:5px; margin-left:90px;" href="http://127.0.0.1:8000/products/4cgb3d5f1d/" class="btn btn-primary">Xem ngay</a></div>
            <div class="progress-bar" style="animation-duration: ${duration}s;"></div>
        </div>
    `, 'custom', duration).dismissOthers();
}


// hiển thị section
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section-content').forEach(function (section) {
        section.classList.remove('active-section')
    })
    // Show the selected section
    document.getElementById(sectionId).classList.add('active-section')
}


// hàm hiển thị thông báo
function showNotification(tag, message) {
    // Cài đặt vị trí thông báo
    alertify.set('notifier', 'position', 'top-right');
    let duration = 5;
    let backgroundColor = '';
    let icon = ""
    switch (tag) {
        // success
        case 's':
            backgroundColor = '#56ed0b'; // Xanh lá
            icon = "https://cdn-icons-png.flaticon.com/512/190/190411.png"
            break;
        // failed
        case 'e':
            backgroundColor = '#fd3e13';
            icon = "https://cdn-icons-png.flaticon.com/512/753/753345.png"
            break;
        // warning
        case 'w':
            backgroundColor = '#e19d14'; // Vàng
            icon = "https://cdn-icons-png.flaticon.com/512/595/595067.png"
            break;
        default:
            backgroundColor = '#ccc'; // Màu xám mặc định nếu tag không hợp lệ
    }

    // Tạo thông báo tùy chỉnh
    alertify.notify(`
        <div class="custom-alertify">
            <img src="${icon}" class="alertify-icon" />
            <div class="alertify-content">
                <strong>${message}</strong></div>
            <div class="progress-bar" style="background-color:${backgroundColor};animation-duration: ${duration}s;"></div>
        </div>
    `, 'custom', duration).dismissOthers();
}

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Gallery filter
        --------------------*/
        $('.featured__controls li').on('click', function () {
            $('.featured__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.featured__filter').length > 0) {
            var containerEl = document.querySelector('.featured__filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
        $("body").addClass("over_hid");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
        $("body").removeClass("over_hid");
    });

    /*------------------
        Navigation
    --------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*-----------------------
        Categories Slider
    ------------------------*/
    $(".categories__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 4,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            0: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 3,
            },

            992: {
                items: 4,
            }
        }
    });


    $('.hero__categories__all').on('click', function () {
        $('.hero__categories ul').slideToggle(400);
    });

    /*--------------------------
        Latest Product Slider
    ----------------------------*/
    $(".latest-product__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------------
        Product Discount Slider
    -------------------------------*/
    $(".product__discount__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            320: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 2,
            },

            992: {
                items: 3,
            }
        }
    });

    /*---------------------------------
        Product Details Pic Slider
    ----------------------------------*/
    $(".product__details__pic__slider").owlCarousel({
        loop: true,
        margin: 20,
        items: 4,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------
        Price Range Slider
    ------------------------ */
    var rangeSlider = $(".price-range"),
        minamount = $("#minamount"),
        maxamount = $("#maxamount"),
        minPrice = rangeSlider.data('min'),
        maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            minamount.val('$' + ui.values[0]);
            maxamount.val('$' + ui.values[1]);
        }
    });
    minamount.val('$' + rangeSlider.slider("values", 0));
    maxamount.val('$' + rangeSlider.slider("values", 1));

    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();

    /*------------------
        Single Product
    --------------------*/
    $('.product__details__pic__slider img').on('click', function () {

        var imgurl = $(this).data('imgbigurl');
        var bigImg = $('.product__details__pic__item--large').attr('src');
        if (imgurl != bigImg) {
            $('.product__details__pic__item--large').attr({
                src: imgurl
            });
        }
    });

    /*-------------------
        Quantity change
    --------------------- */
    var proQty = $('.pro-qty');
    proQty.prepend('<span class="dec qtybtn">-</span>');
    proQty.append('<span class="inc qtybtn">+</span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent().find('input').val(newVal);
    });

})(jQuery);

window.FontAwesomeConfig = {
    searchPseudoElements: true
}

function changeTimeFormat(date) {
    let n = date.toLocaleString([], {
        hour: '2-digit',
        minute: '2-digit',
    });
    return n;
}

$("#commentForm").submit(function (e) {
    e.preventDefault();
    let dt = new Date()
    console.log(dt.getMonth())
    let time = changeTimeFormat(dt) + ", " + dt.getDate() + "/" + (+dt.getMonth() + 1) + "/" + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("Comment Saved to DB...");
            if (res.bool == true) {
                $("#review-res").html("Đã thêm bình luận của bạn")
                $(".hide-comment-form").hide()
                $(".add-review").hide()
                let rating = "";
                for (var i = 1; i <= res.context.rating; i++) {
                    rating += '<i class="fas fa-star text-warning"></i>';
                }
                let _html = `<li>
                          <div class="people-box">
                            <div>
                              <div class="people-image">
                                <img src="https://static-00.iconduck.com/assets.00/avatar-default-icon-1975x2048-2mpk4u9k.png" class="img-fluid blur-up lazyload" alt="" />
                              </div>
                            </div>

                            <div class="people-comment">
                              <a class="name" href="javascript:void(0)">${res.context.user}</a>
                              <div class="date-time">
                                <h6 class="text-content">${time}</h6>

                                <div class="product-rating">
                                  <ul class="rating">${rating}</ul>
                                </div>
                              </div>

                              <div class="reply">
                                <p>${res.context.review}</p>
                              </div>
                            </div>
                          </div>
                        </li>`
                $(".review-list").prepend(_html)
                console.log(_html)
            }
        }
    })
})
// Hàm để lấy giá trị của một tham số từ URL
function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    const regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
    const results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// hiển thị section
function checkSort(sectionId) {
    // Hide all sections
    document.querySelectorAll('.dropdown-item').forEach(function (section) {
        section.classList.remove('active-section')
    })
    // Show the selected section
    document.getElementById(sectionId).classList.add('active-section')
}

// Hàm gọi AJAX để lấy tổng giá từ server
function updateCartTotal() {
    $.ajax({
        url: "/get-cart-total", // URL của view tính tổng giá
        method: "GET",
        success: function(response) {
            // Cập nhật tổng giá trên giao diện
            $('#total-amount').text(response.cart_total_amount.toLocaleString()); // Định dạng số
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}



$(document).ready(function () {

    updateCartTotal(); // Gọi khi tải trang
        
    // Cập nhật mỗi 5 giây (nếu cần liên tục)
    setInterval(updateCartTotal, 5000);

    // lọc sản phẩm
    $(".filter-checkbox").on("click", function () {
        let filter_object = {}
        let sortValue = $('.active-section').attr("value")
        // let sortValue = getParameterByName('sort');
        let min_price = $('input[name="chk[]"]:checked').attr("min")
        let max_price = $('input[name="chk[]"]:checked').attr("max")
        console.log(sortValue)  
        let cpu =  $('input[name="cpu[]"]:checked').attr("value")
        // console.log(cpu)
        let ram =  $('input[name="ram[]"]:checked').attr("value")
        // console.log(ram)
        let tienich =  $('input[name="tienich[]"]:checked').attr("value")
        // console.log(tienich)
        filter_object.min_price = +min_price
        filter_object.max_price = +max_price
        filter_object.cpu = cpu
        filter_object.ram = ram
        filter_object.tienich = tienich
        filter_object.sort = sortValue
        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
                // console.log(filter_key,element.value)
                return element.value
            })
        })
        
        console.log("filter_object",filter_object)
        $.ajax({
            url: "/filter-products",
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
            },
            success: function (response) {
                $("#filtered-product").html(response.data)
            }
        })
    })
    // lọc theo giá cao nhất, khi nó cho số không hợp lệ thì hiện thông báo
    // $("#max_price").on("blur", function () {
    //     let min_price = $(this).attr("min")
    //     let max_price = $(this).attr("max")
    //     let current_price = $(this).val()

    //     console.log("Current Price is:", current_price);
    //     console.log("Max Price is:", max_price);
    //     console.log("Min Price is:", min_price);

    //     if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
    //         // console.log("Price Error Occured");

    //         min_price = Math.round(min_price * 100) / 100
    //         max_price = Math.round(max_price * 100) / 100


    //         // console.log("Max Price is:", min_price);
    //         // console.log("Min Price is:", max_price);

    //         alert("Price must between $" + min_price + ' and $' + max_price)
    //         $(this).val(min_price)
    //         $('#range').val(min_price)

    //         $(this).focus()

    //         return false
    //     }

    // })
    // thêm sản phâm vào giỏ hàng
    $(".add-to-cart-btn").on("click", function () {
        console.log("1")
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()

        let product_id = $(".product-id-" + index).val()
        let product_price = +($(".current-product-price-" + index).text())

        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()


        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Price:", product_price);
        console.log("ID:", product_id);
        console.log("PID:", product_pid);
        console.log("Image:", product_image);
        console.log("Index:", index);
        console.log("Currrent Element:", this_val);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding Product to Cart...");
            },
            success: function (response) {
                // alertify.set('notifier', 'position', 'top-right');
                // alertify.success("Sản phẩm đã được thêm vào giỏ hàng!").dismissOthers();
                showNotification('s', "Sản phẩm đã được thêm vào giỏ hàng!")
                this_val.html("<i style='color:green;' class='d-inline-block  fas fa-check-circle'></i>")
                // this_val.html("✓")
                console.log("Added Product to Cart!");
                $(".cart-items-count").text(response.totalcartitems)
                this_val.prop("disabled", true); // Thay đổi thuộc tính disabled
            }
        })
    })
    // xóa sản phâm trong giỏ hàng
    $(document).on("click", '.delete-product', function () {

        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        // console.log("PRoduct ID:", product_id);
        // console.log("this_val :", this_val);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (response) {
                // alertify.set('notifier', 'position', 'top-right');
                // //  khi nó nổi lên nó sẽ xóa mấy thông báo khác
                // alertify.success("Đã xóa sản phẩm khỏi giỏ hàng!").dismissOthers();
                showNotification('s', "Đã xóa sản phẩm khỏi giỏ hàng!")
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })

    })
    // cập nhật lại số lượng
    $(".update-product").on("click", function () {

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-" + product_id).val()

        // console.log("PRoduct ID:", product_id);
        // console.log("PRoduct QTY:", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (response) {
                alertify.set('notifier', 'position', 'top-right');
                // alertify.success("Cập nhật số lượng thành công!").dismissOthers();
                showNotification('s', "Cập nhật số lượng thành công!")
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
                // window.location.reload()

            }
        })

    })

    // chức năng đặt làm địa chỉ mặc định

    $(document).on("click", ".make-default-address", function () {
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ID is:", id);
        console.log("Element is:", this_val);

        $.ajax({
            url: "/dashboard/address/make-default-address",
            data: {
                "id": id
            },
            dataType: "json",
            success: function (response) {
                // alertify.set('notifier', 'position', 'top-right');
                // alertify.success("Cập nhật địa chỉ thành công!").dismissOthers();
                showNotification("s", "Cập nhật địa chỉ thành công!")
                console.log("Address Made Default....");
                if (response.boolean == true) {

                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check" + id).show()
                    $(".button" + id).hide()

                }
            }
        })
    })

    // thêm sản phẩm ra khỏi danh sách yêu thích
    $(document).on("click", ".add-to-wishlist", function () {
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)


        // console.log("Product ID IS", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Adding to wishlist...")
            },
            success: function (response) {
                // this_val.html("✓")
                this_val.html("<i class='fas fa-heart text-danger'></i>")
                if (response.bool === true) {
                    showNotification("s", "Đã thêm vào danh sách yêu thích!")
                }
            }
        })
    })

    // xóa sản phẩm ra khỏi danh sách yêu thích
    $(document).on("click", ".delete-wishlist-product", function () {
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist id is:", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Deleting product from wishlist...");
            },
            success: function (response) {
                showNotification("s", "Xóa thành công!")
                $("#wishlist-list").html(response.data)
            }
        })
    })
    // chức năng contact
    $(document).on("submit", "#contact-form-ajax", function (e) {
        e.preventDefault()
        console.log("Submited...");

        let full_name = $("#full_name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()

        console.log("Name:", full_name);
        console.log("Email:", email);
        console.log("Phone:", phone);
        console.log("Subject:", subject);
        console.log("MEssage:", message);

        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Sending Data to Server...");
            },
            success: function (res) {
                // alertify.set('notifier', 'position', 'top-right');
                // alertify.success("Gửi thành công").dismissOthers();
                showNotification("s", "Gửi thành công!")
                console.log("Sent Data to server!");
                $("#contact-form-ajax").hide()
                $("#message-response").html("Cảm ơn bạn đã liên hệ với chúng tôi! Chúng tôi sẽ phản hồi trong thời gian sớm nhất.")
            }
        })
    })
})

