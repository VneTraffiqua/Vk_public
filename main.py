import requests
import os
from dotenv import load_dotenv
from pathlib import Path


def save_image(file_path, images_url, settings=None):

    response = requests.get(images_url, params=settings)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_params(url):
    response = requests.get(f'{url}info.0.json')
    response.raise_for_status()
    params_pic = response.json()
    return params_pic['alt'], params_pic['img'], params_pic['num']


if __name__ == '__main__':
    load_dotenv()
    url_comics = 'https://xkcd.com/353/'
    text, img_url, img_id = get_params(url_comics)

    img_path = os.getenv('IMG_PATH')
    Path(f'{img_path}').mkdir(parents=True, exist_ok=True)
    path = Path.cwd() / f'{img_path}' / f'{img_id}.png'
    save_image(path, img_url)
    print(text)

