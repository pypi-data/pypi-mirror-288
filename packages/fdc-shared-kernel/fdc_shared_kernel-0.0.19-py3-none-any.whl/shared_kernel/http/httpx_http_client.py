import httpx

from shared_kernel.interfaces.http import HttpApiClient


class HttpxHttpClient(HttpApiClient):

    async def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
        return response.json()

    async def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, json=json, headers=headers)
        return response.json()

    async def put(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, data=data, json=json, headers=headers)
        return response.json()

    async def delete(self, url: str, headers: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
        return response.json()

    async def patch(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, data=data, json=json, headers=headers)
        return response.json()

    async def head(self, url: str, headers: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.head(url, headers=headers)
        return response.json()

    async def upload_file(self, url: str, file_path: str, filename: str, headers: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            with open(file_path, 'rb') as file:
                response = await client.post(url, files={filename: file}, headers=headers)
        return response.json()

    async def download_file(self, url: str, save_path: str, headers: dict = None) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            with open(save_path, 'wb') as file:
                file.write(await response.read())
