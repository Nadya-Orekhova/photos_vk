import requests
from pprint import pprint

vk_id = input("Введите ID: ")
with open('token.txt', 'r') as f:
    token = f.read()

photos = {}
url = 'https://api.vk.com/method/photos.get'
params = {
    'owner_id': vk_id,
    'album_id': 'profile',
    'v': 5.131,
    'photo_sizes': 1,
    'extended': 1,
    'access_token': token
}
response = requests.get(url, params=params)
# pprint(response.json())
r = response.json()

for i in r['response']['items']:
    img_url = (i['sizes'][-1]['url'])
    img_name = (f'{i["id"]} {i["date"]} {img_url.split("?")[0].split("/")[-1]}')
    up = requests.get(img_url)
    with open(f'photo/{img_name}', 'wb') as file:
        file.write(up.content)


import logging
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG MASSAGE")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("AN ERROR")
logging.critical("A message of CRITICAL severity")



def vk_img(id_user):
    global photos
    photos = {}
    url_vk = 'https://api.vk.com/method/photos.get'
    params = {
        'photo_sizes': 1,
        'owner_id': id_user,
        'v': 5.131,
        'album_id': 'profile',
        'extended': 1,
        'access_token': token
    }

    response = requests.get(url_vk, params=params)
    # pprint(response.json())
    r = response.json()

    for i in r['response']['items']:
        img_url = (i['sizes'][-1]['url'])
        # file_name = str(i['likes']['count']) + '.jpg'
        # photo_sizes = i['sizes'][-1]['type']
        img_name = (f'{i["id"]} {i["date"]} {img_url.split("?")[0].split("/")[-1]}')
        # photos[img_name] = [photo_sizes]
        up = requests.get(img_url)
        photos[img_name] = img_url
        # pprint(photos)
    return photos
def ya_up(token_ya):
    url_ya = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {token_ya}'
    }
    for img_name, img_url in photos.items():
        params = {
            'url': img_url,
            'path': f'{img_name}',
            'disable_redirects': 'true'
        }
        response = requests.post(url_ya, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == '202':
            logging.info(f'File{img_name} have been uploaded successfully.')

    return 'loading is complete'

if __name__ == '__main__':
    vk_img(vk_id)
    token_ya = 'y0_AgAAAAA2DJ8hAADLWwAAAADSx7XTG7leoV3WQc6pIew_M7wuHettd-A'
    ya_up(token_ya)



