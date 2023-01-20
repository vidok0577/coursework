import requests
import json

from datetime import datetime


class YaDisk:
    def __init__(self, token: str):
        self.HOST = 'https://cloud-api.yandex.net:443'
        self.headers = {'Accept': 'application/json', 'Authorization': token}
        self.upload_uri = '/v1/disk/resources/upload'

    def mk_dir(self, dir_name):
        url = self.HOST + '/v1/disk/resources'
        params = {'path': dir_name}
        resp = requests.put(url, headers = self.headers, params=params)
        if resp.status_code == 409:
            print('Такая папка уже существует.')
        else:
            print('Папка создана.')
    
    def upload(self, ext_url: str, file_):
        url = self.HOST + self.upload_uri
        params = {'path': file_, 'url': ext_url}
        upload_resp = requests.post(url, headers=self.headers, params=params)
        if upload_resp.status_code == 200 or 201 or 202:
            print('Файл сохранен.')
        else:
            print('Что-то пошло не так. Код ответа:', upload_resp.status_code)


class Vk:
    def __init__(self, token):
        self.url_api = 'https://api.vk.com/method/'
        self.token = token

    def get_photo_list(self, owner_id, album_id):
        url = self.url_api + 'photos.get'
        params = {'owner_id': owner_id, 'album_id': album_id, 'extended': 1, 'access_token': self.token, 'v': '5.131'}
        resp = requests.get(url=url, params=params)
        return resp.json()


if __name__ == '__main__':
    disk = YaDisk(input('Введите токен Я.Диска: '))
    contact = Vk(input('Введите токен ВК: '))
    owner_id = input('Введите ID пользователя:')
    path_to_backup = 'vk/' + owner_id + '/'
    disk.mk_dir('vk')
    disk.mk_dir(path_to_backup)
    size_dict = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
    foto_list = contact.get_photo_list(owner_id, 'profile')['response']['items']
    likes_count = []
    files_json_info = []

    for foto in foto_list[:5]:
        likes = str(foto['likes']['count'])
        date_uploads = str(datetime.fromtimestamp(foto['date']).strftime('_%d_%m_%Y'))
        file_name = likes if likes not in likes_count else likes + date_uploads
        likes_count.append(likes)
        max_foto = max(foto['sizes'], key = lambda x: size_dict[x['type']])
        size_type = max_foto['type']
        files_json_info.append({'file_name': file_name, 'size': size_type})
        disk.upload(max_foto['url'], path_to_backup + file_name)
    
    with open('files.json', 'w') as f:
        json.dump(files_json_info, f, indent=4)