import requests

from src.core.logger import get_logger, measure_time


class AlbumsClient:

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.endpoint = f"{self.base_url}/albums"
        self.logger = get_logger(self.__class__.__name__)

        # add a new header
        self.session = requests.Session()
        self.session.headers.update({
            "X-Framework": "MiniAPI3-Albums"
        })

    @measure_time
    def get_all_albums(self):
        url = self.endpoint
        self.logger.info(f"GET {url}")
        response = requests.get(url, timeout=self.timeout)
        self.logger.debug(f"Request headers: {self.session.headers}")
        self.logger.info(f"Status code: {response.status_code}")
        return response

    @measure_time
    def get_albums_for_specific_user(self, user_id):
        url = self.endpoint
        params = {"userId": user_id}
        self.logger.info(f"GET {url}")
        response = requests.get(url, params=params, timeout=self.timeout)
        self.logger.info(f"Status code for userId: {user_id} is {response.status_code}")
        return response

