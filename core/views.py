from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
#  cài đặt hiển thị ra màn hình
def index(request):
  username = request.user
  context =  {
    'username':username
  }
  return render(request,"core/index.html",context)