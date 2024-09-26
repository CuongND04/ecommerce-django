from core.models import CartOrderItems,  Product, Category, Vendor, CartOrder, ProductImages, ProductReview, WishList, Address


def default(request):
  categories  = Category.objects.all()

  return {
    "categories":categories,

  }