
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import CartOrderItems, Coupon,  Product, Category, CartOrder, ProductImages, ProductReview, WishList, Address
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


@login_required
def customer_dashboard(request):

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


  user_profile = Profile.objects.get(user=request.user)
  context = {
    "user_profile": user_profile,
    "orders": orders,
    "month": month,
    "total_orders": total_orders,
    'active_section': 'index'
  }
  return render(request,'dashboard/dashboard.html',context)



def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    add = Address.objects.filter(status=True).values().first()
    if add:  # Kiểm tra nếu có dữ liệu
      profile = Profile.objects.get(user=request.user)
      profile.address = add['address']  # Gán giá trị của `address`
      profile.save()  # Lưu thay đổi
      # print(profile.values())
    
    return JsonResponse({"boolean": True})


def profile_user(request):
  user_profile = Profile.objects.get(user=request.user)
  context = {
    "user_profile": user_profile,
    'active_section': 'profile'
  }
  return render(request,'dashboard/profile.html',context)


def address_view(request):
  user_profile = Profile.objects.get(user=request.user)
  address = Address.objects.filter(user=request.user)
  if request.method == "POST":
      address = request.POST.get("address")
      mobile = request.POST.get("mobile")

      new_address = Address.objects.create(
          user=request.user,
          address=address,
          mobile=mobile,
      )
      
      messages.success(request, "Thêm địa chỉ mới thành công.")
      return redirect("dashboard:address")
  else:
      print("Error")
  context = {
    "address": address,
    "user_profile": user_profile,
    'active_section': 'address'
  }
  return render(request,'dashboard/address.html',context)


def order_view(request):
  user_profile = Profile.objects.get(user=request.user)
  orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")

  context = {
    "orders_list": orders_list,
    "user_profile": user_profile,
    'active_section': 'order'
  }
  return render(request,'dashboard/order.html',context)

def order_detail(request, id):
    
    user_profile = Profile.objects.get(user=request.user)
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)

    address = Address.objects.filter(user=request.user)
    context = {
        "order_items": order_items,
        "user_profile": user_profile,
        "orders_list": orders_list,
        "address" : address,
        'active_section': 'order_detail'
    }
    return render(request, 'dashboard/order-detail.html', context)