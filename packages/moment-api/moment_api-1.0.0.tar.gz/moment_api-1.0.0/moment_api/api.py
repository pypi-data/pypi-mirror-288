import requests
import os

class MomentAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://89.23.106.247:5000'  # Replace with your server address

    def generate_text(self, prompt):
        url = f'{self.base_url}/chat'
        data = {'prem_key': self.api_key, 'question': prompt}
        response = requests.post(url, data=data)
        return response.json()['response']

    def generate_image(self, prompt, save_dir='images'):
        url = f'{self.base_url}/generate_image'
        data = {'prem_key': self.api_key, 'prompt': prompt}
        response = requests.post(url, data=data, stream=True)
        if response.status_code == 200:
            image_data = response.content
            filename = f'{prompt}.png'
            filepath = os.path.join(save_dir, filename)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            with open(filepath, 'wb') as f:
                f.write(image_data)
            return f'Изображение успешно сгенерировано и сохранено в {filepath}'
        else:
            return response.json()['message']