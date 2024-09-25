from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ckeditor_cloudinary_uploader import upload_to_cloudinary  # Import hàm upload

# Nếu bạn muốn tạm thời tắt CSRF kiểm tra cho view này (không khuyến khích trừ khi cần thiết):
@csrf_exempt
def ckeditor_image_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        upload_data = upload_to_cloudinary(upload)
        return JsonResponse(upload_data)
    return JsonResponse({'uploaded': False})