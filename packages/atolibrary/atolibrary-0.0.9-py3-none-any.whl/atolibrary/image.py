import requests
from PIL import Image
from io import BytesIO

def show_image(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img.show()
