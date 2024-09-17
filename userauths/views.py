from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

from .models import User
# Create your views here.
def register_view(request):
  if request.method == "POST":
    # lấy dữ liệu từ input bằng request.post
    # or None ở đây là tùy chọn, giúp tránh lỗi nếu dữ liệu không có.
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
      new_user = form.save()
      username = form.cleaned_data.get("username") # form.cleaned_data chứa các dữ liệu đã được xử lý và xác thực từ form.
      messages.success(request,f"Chúc mừng {username}, tài khoản của bạn đã được tạo thành công. ")

      new_user = authenticate(username=form.cleaned_data['email'],password=form.cleaned_data['password1']) # Xác thực thông tin đăng nhập 
      login(request,new_user) #  Nếu xác thực thành công, người dùng sẽ được đăng nhập
      return redirect("core:index")
  else:
    form = UserRegisterForm()

  context = {
    'form':form
  }
  return render(request,"userauths/sign-up.html",context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Bạn đã đăng nhập.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email") 
        password = request.POST.get("password") 
        print(email,password)
        try:
            user = User.objects.get(email=email)
            print("user: ",user)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Bạn vừa đăng nhập thành công.")
                next_url = request.GET.get("next", 'core:index')
                return redirect(next_url)
            else:
                messages.warning(request, "Tài khoản hoặc mật khẩu không chính xác.")
    
        except:
            messages.warning(request, f"Tài khoản với \"{email}\" không tồn tại")
        

    
    return render(request, "userauths/sign-in.html")

def logout_view(request):
   logout(request)
   messages.success(request,"Bạn đã đăng xuất.")
   return redirect("userauths:sign-in")