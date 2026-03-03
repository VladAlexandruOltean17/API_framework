import requests
from src.core.logger import get_logger, measure_time


class CommentsClient:
    """
    Client pentru endpoint-ul /posts.
    """

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.endpoint = f"{self.base_url}/comments"
        self.logger = get_logger(self.__class__.__name__)

        # add a new header
        self.session = requests.Session()
        self.session.headers.update({
            "X-Framework": "MiniAPI3-Comments"
        })

    @measure_time
    def get_comments_by_post(self, post_id: int):
        url = self.endpoint
        params = {"postId": post_id}
        self.logger.info(f"GET {url} params={params}")
        response = requests.get(url, params=params, timeout=self.timeout)
        self.logger.debug(f"Request headers: {self.session.headers}")  # display headers in logs as debug
        self.logger.info(f"Status code pentru postId={post_id}: {response.status_code}")
        return response
