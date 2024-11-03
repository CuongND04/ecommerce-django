from django.urls import path
from userauths import views

app_name = "userauths"
urlpatterns = [
    path("sign-up",views.register_view,name="sign-up"),
    path("sign-in",views.login_view,name="sign-in"),
    path("sign-out",views.logout_view,name="sign-out"),
    
    path("profile/update/", views.profile_update, name="profile-update"),
    path("change-password/",views.change_password, name="change-password"),

    path("forgotpass",views.forgotpass, name="forgotpass"),
    path("reset_password",views.reset_password,name="reset_password"),
]


