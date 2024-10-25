from django.urls import *
from dashboard.views import *

# cài đặt các route trang web 
app_name = "dashboard"

urlpatterns = [
  # home
  path("", customer_dashboard, name="index"),
  path("profile/", profile_user, name="profile"),
  # path("/order/<int:id>", order_detail, name="order-detail"),
  path("address/", address_view, name="address"),
  path("order/", order_view, name="order"),
  path("order/detail/<int:id>", order_detail, name="order-detail"),

  path("/address/make-default-address/", make_address_default, name="make-default-address"),
]