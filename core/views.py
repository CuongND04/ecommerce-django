from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import CartOrderItems,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address
from taggit.models import Tag
from django.db.models import *
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
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

  productSaleOff= Product.objects.all()
  productSaleOff = sorted(productSaleOff, key= lambda Product: -Product.get_percentage())
  context =  {
    'username':username,
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
  for p in productSaleOff[0:4]:
    print(p.get_percentage())
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
  for p in products.values():
    print(p)
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
