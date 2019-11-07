import os
import shutil

import requests
from lxml import html

from config import UPLOADED_FILES_PATH


def get_profile_picture(response):
    tree = html.fromstring(response.content)
    profile_url = tree.xpath('//div[@class="ProfileAvatar"]/a/@href')
    return profile_url


def save_file_to_fs(profile_url, handle):
    profile_img_response = requests.get(profile_url, stream=True)
    if profile_img_response.status_code == 200:
        with open(os.path.join(UPLOADED_FILES_PATH, f'{handle}.jpg'), 'wb') as f:
            profile_img_response.raw.decode_content = True
            shutil.copyfileobj(profile_img_response.raw, f)
    return profile_img_response.status_code
