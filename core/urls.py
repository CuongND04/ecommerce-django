from django.urls import path
from core.views import *

# cài đặt các route trang web 
app_name = "core"

urlpatterns = [
  path("",index,name="index"),
  path("products/",product_list_view,name="product-list"),
  path("category/<cid>/",category_product_list_view,name="category-product-list"),

  path("vendor/",vendor_list_view,name="vendor-list"),
  path("vendor/<vid>",vendor_detail_view,name="vendor-detail")
]