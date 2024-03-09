from PIL import Image
import requests
from io import BytesIO


def get_most_common_color(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    img = img.resize((100, 100))
    pixels = img.getdata()
    color_count = {}
    for pixel in pixels:
        color_count[pixel] = color_count.get(pixel, 0) + 1
    most_common_color = max(color_count, key=color_count.get)
    return most_common_color
