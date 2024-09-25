from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import CartOrderItems,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address
from taggit.models import Tag
# Create your views here.
#  cài đặt hiển thị ra màn hình
def index(request):
  username = request.user
  # lấy ra tất cả sản phẩm trong model Product
  # products = Product.objects.all()
  products = Product.objects.filter(product_status="published")
  productFeatured = Product.objects.filter(product_status="published",featured=True)
  # lấy ra sản phẩm mới nhất
  productLatest = Product.objects.order_by('-date')
  # lấy ra các nhãn
  categories  = Category.objects.all()

  productSaleOff= Product.objects.all()
  productSaleOff = sorted(productSaleOff, key= lambda Product: -Product.get_percentage())
  context =  {
    'username':username,
    "products":products,
    "productFeatured":productFeatured,
    "categories":categories,
    "productLatestOne":productLatest[0:3],
    "productLatestTwo":productLatest[3:6],
    "productSaleOff":productSaleOff[0:4]
  }
  return render(request,"core/index.html",context)

def product_list_view(request):
  # tìm tất cả sản phẩm được phát hành
  products = Product.objects.filter(product_status="published")
  # lấy ra các nhãn
  categories  = Category.objects.all()
  # lấy ra sản phẩm mới nhất
  productLatest = Product.objects.order_by('-date')
  # lấy ra các sản phẩm được giảm giá nhiều nhất
  productSaleOff= Product.objects.all()
  productSaleOff = sorted(productSaleOff, key= lambda Product: -Product.get_percentage())
  for p in productSaleOff[0:4]:
    print(p.get_percentage())
  context = {
    "products":products,
    "categories":categories,
    "productLatestOne":productLatest[0:3],
    "productLatestTwo":productLatest[3:6],
    "productSaleOff":productSaleOff[0:4]
  }
  return render(request,'core/product-list.html',context)

def category_product_list_view(request,cid):
  categories  = Category.objects.all()
  category = Category.objects.get(cid=cid)
  products = Product.objects.filter(product_status="published",category=category)
  # lấy ra các sản phẩm được giảm giá nhiều nhất
  productSaleOff= Product.objects.all()
  productSaleOff = sorted(productSaleOff, key= lambda Product: -Product.get_percentage())
  for p in products.values():
    print(p)
  context = {
    "category":category,
    "products":products,
    "categories":categories,
    "productSaleOff":productSaleOff[0:4]
  }
  return render(request,'core/category-product-list.html',context)

def vendor_list_view(request):
  vendors = Vendor.objects.all();
  categories  = Category.objects.all()
  context = {
    "vendors" : vendors,
    "categories":categories,
  }
  return render(request,"core/vendor-list.html",context)

def vendor_detail_view(request,vid):
  vendor = Vendor.objects.get(vid=vid);
  products = Product.objects.filter(product_status="published",vendor=vendor)
  categories  = Category.objects.all()
  productLatest = Product.objects.order_by('-date')
  context = {
    "vendor" : vendor,
    "categories":categories,
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
  productLatest = Product.objects.order_by('-date')
  categories  = Category.objects.all()
  context  = {
    "product":product,
    "p_images":p_images,
    "categories":categories,
    "productLatestOne":productLatest[0:3],
    "productLatestTwo":productLatest[3:6],
    "products":products
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
