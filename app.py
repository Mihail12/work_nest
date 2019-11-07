import os
import requests

from flask import request, abort

from config import create_app, TWITTER_BASE_URL, UPLOADED_FILES_PATH, STATIC
from utils import get_profile_picture, save_file_to_fs

app = create_app()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/scrape/', methods=['POST'])
def scrape():
    json_data = request.get_json()  # if application/json
    parameters = request.values   # if application/x-www-form-urlencoded
    content = json_data or parameters
    if not content.get('handle'):
        return 'There is no parameter handle', 400
    data, code = 'successful', 200

    handle = content['handle']
    twitter_response = requests.get(f'{TWITTER_BASE_URL}{handle}')
    if twitter_response.status_code == 200:
        profile_url = get_profile_picture(twitter_response)
        if profile_url:
            img_response_status = save_file_to_fs(profile_url[0], handle)
            if img_response_status != 200:
                data, code = 'There is error while getting image', img_response_status
        else:
            data, code = 'There is an issue with scraping profile url', 500
    elif twitter_response.status_code == 404:
        data, code = f'Twitter has no handle with name: {handle}', twitter_response.status_code
    else:
        data, code = 'There is error with connection to twitter', twitter_response.status_code
    return data, code


@app.route('/user/<handle>/profile_pic/', methods=['GET'])
def get_profile_pic(handle):
    picture_path = os.path.join(UPLOADED_FILES_PATH, f'{handle}.jpg')
    if os.path.exists(picture_path):
        return f"<a href='{request.host_url}{STATIC}/{handle}.jpg'>{request.host_url}{STATIC}/{handle}.jpg<a>"
    else:
        abort(404)


@app.route('/users/', methods=['GET'])
def get_all_users():
    files_list = []
    for item in os.listdir(UPLOADED_FILES_PATH):
        picture_url = f"<a href='{request.host_url}{STATIC}/{item}'>{request.host_url}{STATIC}/{item}<a>"
        handle = item.replace('.jpg', '')
        files_list.append(f'{handle}: {picture_url}')
    if files_list:
        return "<br>".join(files_list)
    else:
        return 'There is no scraped users', 404


if __name__ == '__main__':
    app.run()
