import typing as tp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry  # type: ignore


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
        timeout: float = 20.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:  # type: ignore
        url = f"{self.base_url}/{url}"

        http = requests.Session()

        retries = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET"],
        )

        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        http.hooks["response"] = [assert_status_hook]

        http.mount(url, HTTPAdapter(max_retries=retries))

        if kwargs:
            request = http.get(url=url, timeout=self.timeout, params=kwargs["params"])
        else:
            request = http.get(url=url, timeout=self.timeout)
        return request

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:  # type: ignore
        url = f"{self.base_url}/{url}"

        http = requests.Session()

        retries = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["POST"],
        )

        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        http.hooks["response"] = [assert_status_hook]

        http.mount(url, HTTPAdapter(max_retries=retries))

        if kwargs:
            request = http.post(
                url=url,
                timeout=kwargs["timeout"] if "timeout" in kwargs else self.timeout,
                data=kwargs["data"],
            )
        else:
            request = http.post(url=url, timeout=self.timeout)
        return request
