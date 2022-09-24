import requests
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path


def get_random_xkcd():
    url_random_comics = 'https://c.xkcd.com/random/comic/'
    response = requests.get(url_random_comics)
    response.raise_for_status()
    return response.url


def save_image(file_path, images_url, settings=None):
    response = requests.get(images_url, params=settings)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_xkcd_comic_params(url):
    response = requests.get(f'{url}info.0.json')
    response.raise_for_status()
    params_pic = response.json()
    return params_pic['alt'], params_pic['img'], params_pic['num']


def get_address_for_upload_img(token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': 5.131,
        'group_id': group_id,
    }
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_img_to_server(url, path):
    with open(path, 'rb') as img_path:
        files = {
            'file1':  img_path
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    load_options = response.json()
    return load_options['server'], load_options['hash'], load_options['photo']


def save_img_to_vk(token, server_id, img_hash, photos, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'server': server_id,
        'access_token': token,
        'v': 5.131,
        'group_id': group_id,
        'hash': img_hash,
        'caption': 'Its fun',
        'photo': photos,
    }
    response = requests.post(url, params)
    response.raise_for_status()
    response_params = response.json()['response'][0]
    return response_params['owner_id'], response_params['id']


def make_wall_post_vk(token, owner_id, pic_id, message, group_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': token,
        'v': 5.131,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': message,
        'attachments': [f'photo{owner_id}_{pic_id}'],
    }
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    img_path = os.getenv('IMG_PATH')
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    my_group_id = os.getenv('GROUP_ID')
    url_comics = get_random_xkcd()
    try:
        text, img_url, img_id = get_xkcd_comic_params(url_comics)
        Path(f'{img_path}').mkdir(parents=True, exist_ok=True)
        path = Path.cwd() / f'{img_path}' / f'{img_id}.png'
        save_image(path, img_url)
        server_url = get_address_for_upload_img(vk_token, my_group_id)
        server_id, img_hash, photos = upload_img_to_server(server_url, path)
        owner_id, img_id = save_img_to_vk(
            vk_token, server_id, img_hash, photos, my_group_id
        )
        make_wall_post_vk(vk_token, owner_id, img_id, text, my_group_id)
    finally:
        shutil.rmtree(img_path)
