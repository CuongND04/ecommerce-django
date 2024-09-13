from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
# Create your views here.
def register_view(request):
  if request.method == "POST":
    # lấy dữ liệu từ input bằng request.post
    # or None ở đây là tùy chọn, giúp tránh lỗi nếu dữ liệu không có.
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
      new_user = form.save()
      username = form.cleaned_data.get("username") # form.cleaned_data chứa các dữ liệu đã được xử lý và xác thực từ form.
      messages.success(request,f"Hey {username}, Your account was created successfully")

      new_user = authenticate(username=form.cleaned_data['email'],password=form.cleaned_data['password1']) # Xác thực thông tin đăng nhập 
      login(request,new_user) #  Nếu xác thực thành công, người dùng sẽ được đăng nhập
      return redirect("core:index")
  else:
    form = UserRegisterForm()

  context = {
    'form':form
  }
  return render(request,"userauths/sign-up.html",context)