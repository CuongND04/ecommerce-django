from django.contrib import admin
from userauths.models import User,ContactUs
# Register your models here.

# cài đặt những thông tin của admin sẽ hiển thị trong trang admin
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']

# để hiển thị user trong admin page
admin.site.register(User,UserAdmin)
admin.site.register(ContactUs,ContactUsAdmin)
