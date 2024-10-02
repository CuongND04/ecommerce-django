from core.models import CartOrderItems,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address


def default(request):
  categories  = Category.objects.all()
  vendors = Vendor.objects.all()
  return {
    "categories":categories,
    "vendors":vendors
  }