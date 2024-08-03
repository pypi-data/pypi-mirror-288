import requests
import json
import time
import base64
import os
from PIL import Image
from io import BytesIO

class Kandinsky:
    def __init__(self, api_key, secret_key):
        self.URL = 'https://api-key.fusionbrain.ai/key/api/v1/'
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        try:
            response = requests.get(self.URL + 'models', headers=self.AUTH_HEADERS)
            response.raise_for_status()
            data = response.json()
            return data[0]['id']
        except requests.RequestException as e:
            print(f"Error fetching model: {e}")
            return None

    def generate_image(self, prompt, scale='1:1', style='UHD', negative_prompt="Яркие цвета, кислотные цвета", path='./image/generated_image.jpg'):
        if len(prompt) > 1000:
            return "Количество символов превышено, должно быть меньше 1000."
        
        try:
            width, height = self._get_max_resolution(scale)
            model_id = self.get_model()
            
            if not model_id:
                return "Не удалось получить ID модели"
            
            params = {
                "type": "GENERATE",
                "style": style,
                "numImages": 1,
                "width": width,
                "height": height,
                "generateParams": {
                    "query": prompt
                }
            }

            if negative_prompt:
                params["negativePromptUnclip"] = negative_prompt

            data = {
                'model_id': (None, model_id),
                'params': (None, json.dumps(params), 'application/json')
            }

            response = requests.post(self.URL + 'text2image/run', headers=self.AUTH_HEADERS, files=data)
            response.raise_for_status()
            response_data = response.json()
            request_id = response_data['uuid']
            image_base64 = self._check_generation(request_id)
            
            if image_base64:
                self._save_image(image_base64[0], path)
                return "Изображение сгенерировано и сохранено."
            else:
                return "Ошибка при генерации изображения"
        except requests.RequestException as e:
            return f"Ошибка при запросе: {e}"

    def _check_generation(self, request_id, attempts=10, delay=10):
        try:
            while attempts > 0:
                response = requests.get(self.URL + f'text2image/status/{request_id}', headers=self.AUTH_HEADERS)
                response.raise_for_status()
                data = response.json()
                if data['status'] == 'DONE':
                    return data['images']
                elif data['status'] == 'FAIL':
                    raise Exception(f"Generation failed: {data.get('errorDescription', 'Unknown error')}")
                attempts -= 1
                time.sleep(delay)
            raise Exception('Status check failed after multiple attempts')
        except requests.RequestException as e:
            raise Exception(f"Ошибка при проверке статуса: {e}")

    def _get_max_resolution(self, scale):
        max_width = 1024
        max_height = 1024

        try:
            w_ratio, h_ratio = map(int, scale.split(':'))
        except ValueError:
            raise ValueError("Некорректный формат соотношения сторон. Используйте формат 'w:h'.")

        if w_ratio > h_ratio:
            width = max_width
            height = int(max_width * h_ratio / w_ratio)
        else:
            height = max_height
            width = int(max_height * w_ratio / h_ratio)

        return width, height

    def _save_image(self, base64_str, output_file):
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            image_data = base64.b64decode(base64_str)
            image = Image.open(BytesIO(image_data))
            image.save(output_file)
        except Exception as e:
            print(f"Ошибка при сохранении изображения: {e}")

def styles():
    url = "https://cdn.fusionbrain.ai/static/styles/api"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [style["name"] for style in data]
    except requests.RequestException as e:
        raise Exception(f"Ошибка при запросе: {e}")