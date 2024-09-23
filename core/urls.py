from django.urls import path
from core.views import *

# cài đặt các route trang web 
app_name = "core"

urlpatterns = [
  # home
  path("",index,name="index"),
  # product
  path("products/",product_list_view,name="product-list"),
  path("products/<pid>/",product_detail_view,name="product-detail"),
  # category
  path("category/<cid>/",category_product_list_view,name="category-product-list"),
  # vendor
  path("vendor/",vendor_list_view,name="vendor-list"),
  path("vendor/<vid>/",vendor_detail_view,name="vendor-detail"),
  # tags
  path("products/tag/<slug:tag_slug>/",tag_list_request,name="tags"),
  
]