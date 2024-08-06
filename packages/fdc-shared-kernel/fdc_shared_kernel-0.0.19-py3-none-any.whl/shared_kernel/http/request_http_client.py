import requests

from shared_kernel.interfaces.http import HttpApiClient


class RequestsHttpClient(HttpApiClient):

    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        response = requests.post(url, data=data, json=json, headers=headers)
        return response.json()

    def put(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        response = requests.put(url, data=data, json=json, headers=headers)
        return response.json()

    def delete(self, url: str, headers: dict = None) -> dict:
        response = requests.delete(url, headers=headers)
        return response.json()

    def patch(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        response = requests.patch(url, data=data, json=json, headers=headers)
        return response.json()

    def head(self, url: str, headers: dict = None) -> dict:
        response = requests.head(url, headers=headers)
        return response.json()

    def upload_file(self, url: str, file_path: str, filename: str, headers: dict = None) -> dict:
        with open(file_path, 'rb') as file:
            response = requests.post(url, files={filename: file}, headers=headers)
        return response.json()

    def download_file(self, url: str, save_path: str, headers: dict = None) -> None:
        response = requests.get(url, headers=headers)
        with open(save_path, 'wb') as file:
            file.write(response.content)
