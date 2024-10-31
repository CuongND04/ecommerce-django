from core.models import CartOrderItems,  Product, Category, CartOrder, ProductImages, ProductReview, WishList, Address
from django.db.models import Min,Max
from django.contrib import messages 

def default(request):
  categories  = Category.objects.all()
  # vendors = Vendor.objects.all()
  username = request.user
  min_max_price = Product.objects.aggregate(Min("price"),Max("price"))
  # profile = request.user.profile
  # if hasattr(request.user, 'profile'):
  #   profile = request.user.profile
  #   # Tiếp tục truy cập các thuộc tính của profile...
  # else:
  #   print("User chưa có Profile.")  
     
  if request.user.is_authenticated:
    try:
        wishlist = WishList.objects.filter(user=request.user)
    except:
        messages.warning(request, "Bạn cần đăng nhập trước.")
        wishlist = 0
  else:
      wishlist = 0

# tổng tiền giỏ hàng
  cart_total_amount = 0
  if 'cart_data_obj' in request.session:
      for p_id, item in request.session['cart_data_obj'].items():
          cart_total_amount += int(item['qty']) * float(item['price'])
  
  return {
    "categories":categories,
    # "vendors":vendors,
    'wishlist':wishlist,
    "min_max_price":min_max_price,
    "username":username,
    "cart_total_amount":cart_total_amount
    # "profile":profile
  }