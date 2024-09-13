from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate
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

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
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
                messages.success(request, "You are logged in.")
                next_url = request.GET.get("next", 'core:index')
                return redirect(next_url)
            else:
                messages.warning(request, "User Does Not Exist, create an account.")
    
        except:
            messages.warning(request, f"User with {email} does not exist")
        

    
    return render(request, "userauths/sign-in.html")