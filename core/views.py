from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from core.models import CartOrderItems,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address


# Create your views here.
#  cài đặt hiển thị ra màn hình
def index(request):
  username = request.user
  # lấy ra tất cả sản phẩm trong model Product
  # products = Product.objects.all()
  products = Product.objects.filter(product_status="published")
  productFeatured = Product.objects.filter(product_status="published",featured=True)
  # for p in productFeatured.values():
  #   print(p)
  categories  = Category.objects.all()
  # for c in categories.values():
  #   print(c)
  context =  {
    'username':username,
    "products":products,
    "productFeatured":productFeatured,
    "categories":categories
  }
  return render(request,"core/index.html",context)