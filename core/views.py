from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import CartOrderItems, Coupon,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address
from taggit.models import Tag
from django.db.models import *
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from userauths.models import ContactUs,Profile
from django.contrib.auth.decorators import *

from django.core import serializers
# tính năng paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

import calendar
from django.db.models.functions import ExtractMonth
# Create your views here.
#  cài đặt hiển thị ra màn hình
def index(request):
  # lấy ra tất cả sản phẩm trong model Product
  # products = Product.objects.all()
  products = Product.objects.filter(product_status="published")
  productFeatured = Product.objects.filter(product_status="published",featured=True)
  # lấy ra sản phẩm mới nhất
  productLatest = Product.objects.order_by('-date')

  productSaleOff= Product.objects.all()
  productSaleOff = sorted(productSaleOff, key= lambda Product: -Product.get_percentage())
  context =  {
    "products":products,
    "productFeatured":productFeatured,
    "productLatestOne":productLatest[0:3],
    "productLatestTwo":productLatest[3:6],
    "productSaleOff":productSaleOff[0:4]
  }
  return render(request,"core/index.html",context)

def product_list_view(request):
  # tìm tất cả sản phẩm được phát hành
  products = Product.objects.filter(product_status="published")
  # lấy ra sản phẩm mới nhất
  productLatest = Product.objects.order_by('-date')
  # lấy ra các sản phẩm được giảm giá nhiều nhất
  productSaleOff= Product.objects.all()
  productSaleOff = sorted(productSaleOff, key= lambda Product: -Product.get_percentage())
  # for p in productSaleOff[0:4]:
  #   print(p.get_percentage())
  context = {
    "products":products,
    "productLatestOne":productLatest[0:3],
    "productLatestTwo":productLatest[3:6],
    "productSaleOff":productSaleOff[0:4]
  }
  return render(request,'core/product-list.html',context)

def category_product_list_view(request,cid):
  category = Category.objects.get(cid=cid)
  products = Product.objects.filter(product_status="published",category=category)
  # lấy ra các sản phẩm được giảm giá nhiều nhất
  productSaleOff= Product.objects.all()
  productSaleOff = sorted(productSaleOff, key= lambda Product: -Product.get_percentage())
  # for p in products.values():
  #   print(p)
  context = {
    "category":category,
    "products":products,
    "productSaleOff":productSaleOff[0:4]
  }
  return render(request,'core/category-product-list.html',context)

def vendor_list_view(request):
  vendors = Vendor.objects.all();
  context = {
    "vendors" : vendors,
  }
  return render(request,"core/vendor-list.html",context)

def vendor_detail_view(request,vid):
  vendor = Vendor.objects.get(vid=vid);
  products = Product.objects.filter(product_status="published",vendor=vendor)
  productLatest = Product.objects.order_by('-date')
  context = {
    "vendor" : vendor,
    "products":products,
    "productLatestOne":productLatest[0:3],
    "productLatestTwo":productLatest[3:6],
  }
  return render(request,"core/vendor-detail.html",context)

def product_detail_view(request,pid):
  product = Product.objects.get(pid=pid)
  products = Product.objects.filter(category = product.category).exclude(pid=pid)[:4]
  #  lấy hết hình ảnh của sản phẩm
  p_images = product.p_images.all()

  # Lấy đánh giá sản phẩm
  reviews = ProductReview.objects.filter(product=product).order_by('-date')
  # Tính đánh giá trung bình
  average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg("rating"))
  productLatest = Product.objects.order_by('-date')
  # Product Review Form
  review_form = ProductReviewForm()
  # Mỗi người dùng chỉ được comment một lần
  make_review = True
  if request.user.is_authenticated:
    user_review_count = ProductReview.objects.filter(user=request.user,product = product).count()
    if user_review_count > 0:
      make_review = False
  context  = {
    "product":product,
    "p_images":p_images,
    "productLatestOne":productLatest[0:3],
    "productLatestTwo":productLatest[3:6],
    "products":products,
    "reviews":reviews,
    "average_rating":average_rating,
    "review_form":review_form,
    "make_review":True
  }
  return render(request,"core/product-detail.html",context)

def tag_list_request(request,tag_slug = None):
  products = Product.objects.filter(product_status="published").order_by("-id")
  tag = None
  if tag_slug:
    tag = get_object_or_404(Tag,slug=tag_slug)
    products = products.filter(tags__in=[tag])
  context = {
    "products" : products,
    "tag":tag
  }
  return render(request,"core/tag.html",context)

def ajax_add_review(request,pid):
  product = Product.objects.get(pk = pid)
  user = request.user

  review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

  context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }
  average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
  return JsonResponse(
       {
         'bool': True,
        'context': context,
        'average_reviews': average_reviews
       }
    )

def search_view(request):
  query = request.GET.get("q")
  products = Product.objects.filter(title__icontains=query).order_by("-date")
  context = {
    "products":products,
    "query":query
  }
  return render(request,"core/search.html",context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte = min_price)
    products = products.filter(price__lte = max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct() 
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct() 
  
    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})

def add_to_cart(request):
    
    #  lưu trữ thông tin của sản phẩm được thêm vào giỏ hàng.
    cart_product = {}
    # Thông tin sản phẩm được lấy từ các tham số của yêu cầu GET
    product = Product.objects.get(pid=request.GET['pid'])
    
    # Tạo một mục mới trong cart_product với khóa là id của sản phẩm
    cart_product[str(request.GET['id'])] = {
        'title': product.title,
        'qty': request.GET['qty'],
        # price mặc định là decimal nên phải chuyển qua kiểu khác
        'price': str(product.price),
        'image': product.image.url,
        'pid': request.GET['pid'],
    }
    # print( cart_product[str(request.GET['id'])]['price'])
    if 'cart_data_obj' in request.session:
        # Nếu cart_data_obj (giỏ hàng) đã tồn tại trong session, 
        # thì kiểm tra xem sản phẩm với ID cụ thể này đã có trong giỏ hàng hay chưa.
        if str(request.GET['id']) in request.session['cart_data_obj']:
            # Nếu sản phẩm đã có trong giỏ hàng, mã sẽ cập nhật 
            # số lượng (qty) của sản phẩm đó trong session.

            # Lấy dữ liệu giỏ hàng hiện tại từ session và gán vào cart_data.
            cart_data = request.session['cart_data_obj']
            # Cập nhật số lượng (qty) của sản phẩm trong 
            # cart_data bằng giá trị mới từ cart_product.
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])

            cart_data.update(cart_data)
            # Lưu cart_data đã cập nhật lại vào session.
            request.session['cart_data_obj'] = cart_data
            
        else:
            # Nếu sản phẩm chưa có trong giỏ hàng:
            
            # print(product.price)
            # cart_product[str(request.GET['id'])]['price'] = product.price
            #Lấy giỏ hàng hiện tại từ session.
            cart_data = request.session['cart_data_obj']
            # Thêm cart_product vào cart_data bằng phương thức update.
            cart_data.update(cart_product)
            # Lưu lại cart_data đã cập nhật vào session.
            request.session['cart_data_obj'] = cart_data

    else: # Nếu cart_data_obj chưa tồn tại trong session:
        
        # Tạo một giỏ hàng mới (cart_data_obj) với cart_product 
        # là sản phẩm đầu tiên và lưu vào session.
        request.session['cart_data_obj'] = cart_product


      #Trả về một phản hồi JSON chứa hai thông tin:
      # data: là giỏ hàng hiện tại sau khi thêm sản phẩm, lấy từ session.
      # totalcartitems: là tổng số lượng sản phẩm trong giỏ hàng, tính bằng độ dài của cart_data_obj
    
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def cart_view(request):
  cart_total_amount = 0
  if 'cart_data_obj' in request.session:
      for p_id, item in request.session['cart_data_obj'].items():
          print("item",item)
          cart_total_amount += int(item['qty']) * float(item['price'])
      return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
  else:
      messages.warning(request, "Your cart is empty")
      return redirect("core:index")
  
def delete_item_from_cart(request):
    # lấy id của sản phâm bị xóa
    product_id = str(request.GET['id'])
    # kiểm tra có id của giỏ hàng trong session chưa
    if 'cart_data_obj' in request.session:
        # kiểm tra xem có id của sp đó trong giỏ hàng không
        if product_id in request.session['cart_data_obj']:
            # lấy dữ liệu giỏ hàng về biến 
            cart_data = request.session['cart_data_obj']

            # xóa sản phẩm đó
            del request.session['cart_data_obj'][product_id]

            # cập nhật giỏ hàng
            request.session['cart_data_obj'] = cart_data
    # tính toán lại tổng giá khi xóa sản phẩm
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])}) 

@login_required
def checkout_view(request):

  cart_total_amount = 0
  total_amount = 0
  if 'cart_data_obj' in request.session:
    for p_id, item in request.session['cart_data_obj'].items():
      total_amount += int(item['qty']) * float(item['price'])

    order = CartOrder.objects.create(
      user = request.user,
      price = total_amount
    )

    for p_id, item in request.session['cart_data_obj'].items():
      cart_total_amount += int(item['qty']) * float(item['price'])

      cart_order_products = CartOrderItems.objects.create(
        order=order,
        invoice_no="INVOICE_NO-" + str(order.id), # INVOICE_NO-5,
        item=item['title'],
        image=item['image'],
        qty=item['qty'],
        price=item['price'],
        total=float(item['qty']) * float(item['price'])
      )


  host = request.get_host()
  paypal_dict = {
    'business' : settings.PAYPAL_RECEIVER_EMAIL,
    'amount': cart_total_amount,
    'item_name': "Order-Item-No-"+str(order.id),
    'invoice': 'INVOICE_NO-'+str(order.id),
    "currency_code":"USD",
    "notify_url":"http://{}{}".format(host,reverse("core:paypal-ipn")),
    "return_url":"http://{}{}".format(host,reverse("core:payment-completed")),
    "cancel_url":"http://{}{}".format(host,reverse("core:payment-failed")),
  }
  paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

  # cart_total_amount = 0
  # if 'cart_data_obj' in request.session:
  #   for p_id, item in request.session['cart_data_obj'].items():
  #     cart_total_amount += int(item['qty']) * float(item['price'])

  active_address = Address.objects.get(user=request.user,status = True)



  context = {
    "cart_data":request.session['cart_data_obj'], 
    'totalcartitems': len(request.session['cart_data_obj']), 
    'cart_total_amount':cart_total_amount,
    'paypal_payment_button': paypal_payment_button,
    "active_address": active_address
  }
  return render(request, "core/checkout.html", context)
  
def save_checkout_info(request):
  cart_total_amount = 0
  total_amount = 0
  if request.method == "POST":
    full_name = request.POST.get("full_name")
    email = request.POST.get("email")
    mobile = request.POST.get("mobile")
    address = request.POST.get("address")
    city = request.POST.get("city")
    state = request.POST.get("state")
    country = request.POST.get("country")

    print(full_name)
    print(email)
    print(mobile)
    print(address)
    print(city)
    print(state)
    print(country)

    # gán các thông tin lấy được vào session
    request.session['full_name'] = full_name
    request.session['email'] = email
    request.session['mobile'] = mobile
    request.session['address'] = address
    request.session['city'] = city
    request.session['state'] = state
    request.session['country'] = country


    # Nếu có dữ liệu giỏ hàng cart_data trong session
    if 'cart_data_obj' in request.session:

      # tính tổng số tiền phải thanh toán
      for p_id, item in request.session['cart_data_obj'].items():
          total_amount += int(item['qty']) * float(item['price'])


      request.session['total_amount'] = total_amount

      full_name = request.session['full_name']
      email = request.session['email']
      phone = request.session['mobile']
      address = request.session['address']
      city = request.session['city']
      state = request.session['state']
      country = request.session['country']

      # Create ORder Object
      order = CartOrder.objects.create(
          user=request.user,
          price=total_amount,
          full_name=full_name,
          email=email,
          phone=phone,
          address=address,
          city=city,
          state=state,
          country=country,
      )

      del request.session['full_name']
      del request.session['email']
      del request.session['mobile']
      del request.session['address']
      del request.session['city']
      del request.session['state']
      del request.session['country']

      # Getting total amount for The Cart
      for p_id, item in request.session['cart_data_obj'].items():
          cart_total_amount += int(item['qty']) * float(item['price'])

          cart_order_products = CartOrderItems.objects.create(
              order=order,
              invoice_no="INVOICE_NO-" + str(order.id), # INVOICE_NO-5,
              item=item['title'],
              image=item['image'],
              qty=item['qty'],
              price=item['price'],
              total=float(item['qty']) * float(item['price'])
          )
    return redirect("core:checkout", order.oid)
  return redirect("core:checkout", order.oid) 

def checkout(request, oid):
  order = CartOrder.objects.get(oid=oid)
  order_items = CartOrderItems.objects.filter(order=order)
  old_price = request.session.get('total_amount')
  print("old_price: ",old_price)
  if request.method == "POST":
      code = request.POST.get("code")
      coupon = Coupon.objects.filter(code=code, active=True).first()
      if coupon:
          if coupon in order.coupons.all():
              messages.warning(request, "Mã giảm giá này đã được sử dụng, không thể áp dụng lại.")
              return redirect("core:checkout", order.oid)
          else:
              discount = order.price * coupon.discount / 100 

              order.coupons.add(coupon)
              order.price -= discount
              order.saved += discount
              order.save()
              messages.success(request, "Mã giảm giá đã được áp dụng thành công!")
              return redirect("core:checkout", order.oid)
      else:
          messages.error(request, "Mã giảm giá không hợp lệ, vui lòng kiểm tra lại.")

      

  context = {
     "old_price":old_price,
      "order": order,
      "order_items": order_items,
      # "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,

  }
  return render(request, "core/checkout.html", context)


def create_checkout_session(request, oid):
    order = CartOrder.objects.get(oid=oid)
  # stripe.api_key = settings.STRIPE_SECRET_KEY

  # checkout_session = stripe.checkout.Session.create(
  #     customer_email = order.email,
  #     payment_method_types=['card'],
  #     line_items = [
  #         {
  #             'price_data': {
  #                 'currency': 'USD',
  #                 'product_data': {
  #                     'name': order.full_name
  #                 },
  #                 'unit_amount': int(order.price * 100)
  #             },
  #             'quantity': 1
  #         }
  #     ],
  #     mode = 'payment',
  #     success_url = request.build_absolute_uri(reverse("core:payment-completed", args=[order.oid])) + "?session_id={CHECKOUT_SESSION_ID}",
  #     cancel_url = request.build_absolute_uri(reverse("core:payment-completed", args=[order.oid]))
  # )

  # order.paid_status = False
  # order.stripe_payment_intent = checkout_session['id']
  # order.save()

  # print("checkkout session", checkout_session)
  # return JsonResponse({"sessionId": checkout_session.id})

@login_required
def payment_completed_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    
    if order.paid_status == False:
        order.paid_status = True
        order.save()
        
    context = {
        "order": order,
        # "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'core/payment-completed.html',  context)

@login_required
def payment_failed_view(request):
  return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
  orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
  address = Address.objects.filter(user=request.user)

  # Hàm annotate được dùng để thêm
  #  một trường mới vào mỗi đối tượng trong truy vấn. 
  # Ở đây, trường mới được thêm là month, được lấy 
  # bằng cách sử dụng hàm ExtractMonth("order_date"), tức 
  # là trích xuất tháng từ trường order_date (ngày đặt hàng). Mỗi 
  # đơn hàng sẽ có thêm một thuộc tính month đại diện cho tháng 
  # mà đơn hàng đó được đặt.

  # .values("month") được dùng để tạo một danh sách chỉ chứa giá trị của cột month từ các đơn hàng.

  # lại sử dụng annotate, nhưng lần này là
  #  để thêm trường count, trong đó Count("id") sẽ đếm số lượng đơn hàng có cùng tháng. 
  # Kết quả là, mỗi tháng sẽ có một giá trị count 
  # đại diện cho tổng số đơn hàng trong tháng đó.

  # .values("month", "count") được dùng để chỉ lấy hai trường month và count
  orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
  month = []
  total_orders = []

  for i in orders:
    month.append(calendar.month_name[i["month"]])
    total_orders.append(i["count"])



  if request.method == "POST":
    address = request.POST.get("address")
    mobile = request.POST.get("mobile")

    new_address = Address.objects.create(
        user=request.user,
        address=address,
        mobile=mobile,
    )
    
    messages.success(request, "Thêm địa chỉ mới thành công.")
    return redirect("core:dashboard")
  else:
    print("Error")


  user_profile = Profile.objects.get(user=request.user)
  context = {
    "user_profile": user_profile,
    "orders": orders,
    "orders_list": orders_list,
    "address": address,
    "month": month,
    "total_orders": total_orders,
  }
  return render(request,'core/dashboard.html',context)


def order_detail(request, id):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)

    address = Address.objects.filter(user=request.user)
    context = {
        "order_items": order_items,
        "orders_list": orders_list,
        "address" : address
    }
    return render(request, 'core/order-detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


@login_required
def wishlist_view(request):
    wishlist = WishList.objects.filter(user=request.user)
    context = {
        "wishlist":wishlist
    }
    return render(request, "core/wishlist.html", context)


def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    # print("product id isssssssssssss:" + product_id)

    context = {}

    wishlist_count = WishList.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = WishList.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)

def remove_wishlist(request):
    # Hàm lấy giá trị id từ query string của request HTTP
    pid = request.GET['id']
    # Lọc tất cả các mục trong mô hình WishList thuộc về người dùng hiện tại (request.user).
    wishlist = WishList.objects.filter(user=request.user)
    # lấy một mục cụ thể trong WishList theo id
    wishlist_d = WishList.objects.get(id=pid)
    # xoá sản phẩm khỏi cơ sở dữ liệu.
    delete_product = wishlist_d.delete()
    
    context = {
        "bool":True, # trạng thái thành công
        "wishlist":wishlist # danh sách yêu thích còn lại
    }
    # chuyển đổi danh sách yêu thích (wishlist) sang 
    # định dạng JSON. Dữ liệu này sẽ được trả về cho client.
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('core/async/wishlist-list.html', context)
    return JsonResponse({'data':t,'wishlistp':wishlist_json})

# Other Pages 
def contact(request):
  return render(request, "core/contact.html")

def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data":data})