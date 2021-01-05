import typing as tp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class Session(requests.Session):
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        url = f'{self.base_url}/{url}'
        
        http = requests.Session()

        retries = Retry(
                total=self.max_retries,
                backoff_factor=self.backoff_factor,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["GET"]
        )
        
        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        http.hooks["response"] = [assert_status_hook]

        http = requests.Session()
        http.mount(url, HTTPAdapter(max_retries=retries))

        request = http.get(url, timeout=self.timeout)
        return request

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        pass
    