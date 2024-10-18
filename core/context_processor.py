from core.models import CartOrderItems,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address
from django.db.models import Min,Max
from django.contrib import messages 
def default(request):
  categories  = Category.objects.all()
  vendors = Vendor.objects.all()
  username = request.user
  min_max_price = Product.objects.aggregate(Min("price"),Max("price"))

  if request.user.is_authenticated:
    try:
        wishlist = WishList.objects.filter(user=request.user)
    except:
        messages.warning(request, "Bạn cần đăng nhập trước.")
        wishlist = 0
  else:
      wishlist = 0


  return {
    "categories":categories,
    "vendors":vendors,
    'wishlist':wishlist,
    "min_max_price":min_max_price,
    "username":username
  }