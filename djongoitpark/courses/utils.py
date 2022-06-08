import requests
from django.conf import settings

url = f'https://api.telegram.org/bot{settings.TOKEN}/sendPhoto?chat_id={settings.ADMIN_IDS}'


def send_photo(file):
    x = requests.post(url, files={'photo': file})
    file_id = x.json()['result']['photo'][-1]['file_id']
    return file_id
