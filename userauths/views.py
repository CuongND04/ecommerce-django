from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm,ProfileForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from core.models import *
from userauths.models import Profile, User
from .models import User
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import EmailMessage
# Create your views here.
def register_view(request):
  categories  = Category.objects.all()
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
    'form':form,
    "categories":categories,
  }
  return render(request,"userauths/sign-up.html",context)

def login_view(request):
    categories  = Category.objects.all()
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
                messages.success(request, "Chào mừng bạn! Đăng nhập thành công, cùng bắt đầu nào!")
                next_url = request.GET.get("next", 'core:index')
                return redirect(next_url)
            else:
                messages.warning(request, "Tài khoản hoặc mật khẩu không chính xác.")
    
        except:
            messages.warning(request, f"Tài khoản với \"{email}\" không tồn tại")
        

    context = {
    "categories":categories,
    }
    return render(request, "userauths/sign-in.html",context)

def logout_view(request):
   logout(request)
  #  messages.success(request,"Bạn đã thoát khỏi tài khoản. Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!")
   return redirect("userauths:sign-in")

def profile_update(request):
    user_profile = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
      form = ProfileForm(request.POST, request.FILES, instance=profile)
      if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        messages.success(request, "Cập nhật thành công.")
        return redirect("dashboard:profile")
    else:
      form = ProfileForm(instance=profile)
    print("form:",form)
    context = {
      "form": form,
      "user_profile": user_profile,
      "profile": profile,
      'active_section': 'edit_profile'
    }

    return render(request, "userauths/profile-edit.html", context)


def change_password(request):
    user_profile = Profile.objects.get(user=request.user)
    context={
       "user_profile": user_profile,
       'active_section': 'change_password',
    }
    # ch = register_table.objects.filter(user__id=request.user.id)
    # if len(ch)>0:
    #     data = register_table.objects.get(user__id=request.user.id)
    #     context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        print(check)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Đổi mật khẩu thành công!!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Mật khẩu hiện tại không đúng. Xin vui lòng nhập lại."
            context["col"] = "alert-danger"

    return render(request,"userauths/change-password.html",context)

def forgotpass(request):
    context = {}
    if request.method=="POST":
        email = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,email=email)
        user.set_password(pwd)
        user.save()

        # login(request,user)
        # if user.is_superuser:
        #     return HttpResponseRedirect("/admin")
        # else:
        return HttpResponseRedirect("/user/sign-in")
        # context["status"] = "Password Changed Successfully!!!"

    return render(request,"userauths/forgot_pass.html",context)

import random

def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,email=un)
        otp = random.randint(1000,9999)
        msz = "Xin chào {} \n{} là mã xác thực của bạn (OTP) \nĐừng chia sẻ với bất kì ai \nThanks&Regards \nLapOne".format(user.profile.full_name, otp)
        try:
            email = EmailMessage("Xác thực tài khoản",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except Exception as e:
          import logging
          logging.error("Lỗi khi gửi email: %s", e)
          return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})