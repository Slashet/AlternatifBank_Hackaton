# ...existing code...
import requests

# Define the URL and the path to the image
#image_path = "image.png"  # Update this to your image path
url = "https://customvisioncode-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/dd0a01f3-6338-47e6-9bee-fba004fb3de8/detect/iterations/Iteration5/image"

def request(image_path):
    # Read the image file
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    headers = {
        'Content-Type': 'application/octet-stream',
        'Prediction-Key': '2axxcJkZnbmPICTvkdODQSmvbj84oYoqDA7AlHFbosZAOrxoFn2gJQQJ99BJACfhMk5XJ3w3AAAIACOGXsB3'
    }

    response = requests.post(url, headers=headers, data=image_data)

    return response.json()

# ...existing code...
def upload_image_bytes(image_bytes):
    """
    RAM'deki JPEG/Png byte'larını doğrudan API'ye gönderir.
    image_bytes: bytes veya bytearray
    Döner: API'nin JSON cevabı (dict)
    """
    if not isinstance(image_bytes, (bytes, bytearray)):
        raise TypeError("image_bytes must be bytes or bytearray")

    headers = {
        'Content-Type': 'application/octet-stream',
        'Prediction-Key': '2axxcJkZnbmPICTvkdODQSmvbj84oYoqDA7AlHFbosZAOrxoFn2gJQQJ99BJACfhMk5XJ3w3AAAIACOGXsB3'
    }

    resp = requests.post(url, headers=headers, data=image_bytes)
    return resp.json()
