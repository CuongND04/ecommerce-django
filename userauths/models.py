from django.db import models
from django.contrib.auth.models import AbstractUser 
import cloudinary.models
from django.db.models.signals import post_save
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    
    def __str__(self):
      return self.username
    
class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200) 
    subject = models.CharField(max_length=200) 
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name
    
class Profile(models.Model):

    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = cloudinary.models.CloudinaryField('images', folder="fresh_mart")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True) 
    address = models.CharField(max_length=200, null=True, blank=True) 
    country = models.CharField(max_length=200, null=True, blank=True) 
    verified = models.BooleanField(default=False, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    birthdate = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"
    
# sender: Đối tượng (model) đã gửi signal, trong trường hợp này là model User.

# instance: Thể hiện (instance) của đối tượng vừa được 
# lưu vào cơ sở dữ liệu, ở đây là một đối tượng User.

# created: Biến boolean, nếu True có nghĩa là một đối tượng
# mới vừa được tạo (người dùng mới), nếu False nghĩa là đối tượng đã tồn tại và chỉ được cập nhật.

# kwargs: Các tham số khác có thể được truyền vào
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Hàm này đảm bảo rằng profile của người dùng (được truy cập
#  qua instance.profile) sẽ được lưu mỗi khi đối tượng User được lưu lại.


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# post_save là một loại signal 
# trong Django, được gửi mỗi khi một đối tượng được lưu thành công vào cơ sở dữ liệu.

# hàm này sẽ chạy ngay sau khi một đối tượng User được tạo ra 
post_save.connect(create_user_profile, sender=User)
# được gọi sau khi một đối tượng User được lưu
post_save.connect(save_user_profile, sender=User)    