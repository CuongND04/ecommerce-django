from . import views
from django.urls import path
urlpatterns = [
    path('', views.CreateRoom, name='create-room'),
    path('testchat/', views.MessageView, name='room'),
]