import base64


def base64_to_bytes(base64_image):
    try:
        encoded_data = base64_image.split(',')[1]
        image_bytes = base64.b64decode(encoded_data)
        return image_bytes
    except Exception as e:
        print("[preprocess_chat_messages ]Error:", e)
        return None
