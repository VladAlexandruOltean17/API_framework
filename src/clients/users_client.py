import requests

from src.core.logger import get_logger, measure_time
from src.utils.http import create_session


class UsersClient:
    """
    Client pentru endpoint-ul /users.
    """

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.endpoint = f"{self.base_url}/users"
        self.logger = get_logger(self.__class__.__name__)

        # add a new header, get the create_session method from http
        self.session = create_session()
        self.session.headers.update({
            "X-Framework": "MiniAPI3-Users"
        })

    @measure_time
    def get_all_users(self):
        url = self.endpoint
        self.logger.info(f"GET {url}")
        # response = requests.get(url, timeout=self.timeout)  # create_session() logic from http is completely bypassed
        response = self.session.get(url, timeout=self.timeout)  # this way the create_logic() is used
        # and the retries logic is used as well
        self.logger.debug(f"Request headers: {self.session.headers}")  # display headers in logs as debug
        self.logger.info(f"Status code: {response.status_code}")
        return response

    @measure_time
    def get_user_by_id(self, user_id: int):
        url = f"{self.endpoint}/{user_id}"
        self.logger.info(f"GET {url}")
        response = requests.get(url, timeout=self.timeout)
        self.logger.info(
            f"Status code pentru user_id={user_id}: {response.status_code}"
        )
        return response

    @measure_time
    def get_invalid_user(self, user_id: int):
        url = f"{self.endpoint}/{user_id}"
        self.logger.info((f"GET {url}"))
        response = requests.get(url, timeout=self.timeout)
        self.logger.error(f"The user_id {user_id} you are searching for does not exist")
        self.logger.error(f"The status code is {response.status_code}")
        return response
