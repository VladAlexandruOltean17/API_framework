import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.core.logger import get_logger

logger = get_logger("http.retry")


class LoggingRetryAdapter(HTTPAdapter):
    def __init__(self, retries: int = 3):
        self.retries = retries

        retry = Retry(
            total=retries,
            # status_forcelist=[200], # this is for testing, use 200 to be able to test de retry logic
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            backoff_factor=0,  # no sleep unless you want it
            raise_on_status=False,
        )

        super().__init__(max_retries=retry)

    def send(self, request, **kwargs):
        attempt = 0

        while True:
            attempt += 1
            response = super().send(request, **kwargs)

            if response.status_code < 500:  # use 200 here for testing
                return response

            if attempt < self.retries:
                logger.warning(
                    "Attempt %d/%d failed: %s %s returned %s",
                    attempt,
                    self.retries,
                    request.method,
                    request.url,
                    response.status_code,
                )
            else:
                logger.error(
                    "Final attempt %d/%d failed: %s %s returned %s",
                    attempt,
                    self.retries,
                    request.method,
                    request.url,
                    response.status_code,
                )
                return response


def create_session() -> requests.Session:
    session = requests.Session()
    adapter = LoggingRetryAdapter(retries=3)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session
