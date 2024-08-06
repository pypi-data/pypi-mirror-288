from abc import ABC, abstractmethod


class HttpApiClient(ABC):

    @abstractmethod
    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        pass

    @abstractmethod
    def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        pass

    @abstractmethod
    def put(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        pass

    @abstractmethod
    def delete(self, url: str, headers: dict = None) -> dict:
        pass

    @abstractmethod
    def patch(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> dict:
        pass

    @abstractmethod
    def head(self, url: str, headers: dict = None) -> dict:
        pass

    @abstractmethod
    def upload_file(self, url: str, file_path: str, filename: str, headers: dict = None) -> dict:
        pass

    @abstractmethod
    def download_file(self, url: str, save_path: str, headers: dict = None) -> None:
        pass
