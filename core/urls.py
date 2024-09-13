from django.urls import path
from core.views import index

# cài đặt các route trang web 
app_name = "core"

urlpatterns = [
  path("",index,name="index")
]