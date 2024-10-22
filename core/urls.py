from django.urls import *
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
  # review
  path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),

  # Search
  path("search/",search_view,name="search"),
  # filter 
  path("filter-products/",filter_product,name="filter-product"),
  # add to cart
  path("add-to-cart/",add_to_cart,name="add-to-cart"),
  # xem giỏ hàng  
  path("cart/", cart_view, name="cart"),
  # xóa sản phẩm
  path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
  # cập nhật số lượng từ trang giỏ hàng
  path("update-cart/", update_cart, name="update-cart"),


  path("checkout/<oid>/", checkout, name="checkout"),


  path('paypal/', include('paypal.standard.ipn.urls')),

  path("payment-completed/", payment_completed_view, name="payment-completed"),

  path("payment-failed/", payment_failed_view, name="payment-failed"),
  # Dashboard
  path("dashboard/", customer_dashboard, name="dashboard"),

  path("dashboard/order/<int:id>", order_detail, name="order-detail"),

  # đặt làm địa chỉ mặc định
  path("make-default-address/", make_address_default, name="make-default-address"),
  # thêm vào danh sách yêu thích
  path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),
  path("wishlist/", wishlist_view, name="wishlist"),
  path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),

  path("contact/", contact, name="contact"),

  path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),

   path("save_checkout_info/", save_checkout_info, name="save_checkout_info"),
]