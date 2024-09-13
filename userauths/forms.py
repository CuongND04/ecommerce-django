from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    #  tự khai báo các field để có thể điều chỉnh được (thêm placeholder,css)
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username",'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email",'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password",'class':'form-control','id':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password",'class':'form-control'}))
    class Meta:
        model = User #  để form biết là nó đang làm việc với model User.
        fields = ['username', 'email'] #  các trường mà form sẽ yêu cầu