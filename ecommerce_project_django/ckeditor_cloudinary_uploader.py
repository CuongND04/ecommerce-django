import cloudinary.uploader

def upload_to_cloudinary(file):
    result = cloudinary.uploader.upload(file, folder="fresh_mart")
    return {
        "uploaded": True,
        "url": result["url"]
    }