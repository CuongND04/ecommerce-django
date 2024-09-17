from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from core.models import CartOrderItems,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address

# Create your views here.
#  cài đặt hiển thị ra màn hình
def index(request):
  # lấy ra tất cả sản phẩm trong model Product
  products = Product.objects.all()
  username = request.user
  context =  {
    'username':username,
    "products":products
  }
  return render(request,"core/index.html",context)