from django.contrib import admin
from userauths.models import User
# Register your models here.

# cài đặt những thông tin của admin sẽ hiển thị trong trang admin
class UserAdmin(admin.ModelAdmin):
  list_display = ['username','email','bio']

# để hiển thị user trong admin page
admin.site.register(User,UserAdmin)
