
import requests
import base64

from urllib.parse import urlparse


class Picarta:
    def __init__(self, api_token, url="https://picarta.ai/classify", top_k=10):
        self.api_token = api_token
        self.url = url
        self.top_k = top_k
        self.headers = {"Content-Type": "application/json"}
    
    def is_valid_url(self, input_str):
        try:
            result = urlparse(input_str)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def read_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def localize(self, img_path, center_latitude=None, center_longitude=None, radius=None):
        if self.is_valid_url(img_path):
            image_data = img_path
        else:
            image_data = self.read_image(img_path)
        
        payload = {
            "TOKEN": self.api_token,
            "IMAGE": image_data,
            "TOP_K": self.top_k,
            "Center_LATITUDE": center_latitude,
            "Center_LONGITUDE": center_longitude,
            "RADIUS": radius
        }

        response = requests.post(self.url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

