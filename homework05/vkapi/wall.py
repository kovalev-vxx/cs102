import textwrap
import time
import typing as tp
from itertools import chain
from string import Template

import pandas as pd  # type: ignore
from pandas import json_normalize  # type: ignore
from tqdm import tqdm  # type: ignore

from vkapi import config, session  # type: ignore
from vkapi.exceptions import APIError  # type: ignore


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:

    if count > max_count:
        count = max_count

    count_of_iter = (count + 99) // 100
    code = (
        f"{{"
        f"var doc = [];"
        f"var request_count = {count};"
        f"var i=0;while (i < {count_of_iter}){{"
        f"  var offset = {offset} + i * 100;"
        f"  var docs = API.wall.get({{'owner_id': '{owner_id}', 'extended': '{extended}', 'domain': '{domain}','count': request_count,'offset': offset, 'filter': 'owner','v': '{config.VK_CONFIG['version']}'}});"
        f"  if (request_count > 100) {{request_count = request_count - 100;}}"
        f"  doc.push(docs.items);"
        f"  i = i+1;}}"
        f"return doc;}}"
    )

    response = session.post(
        url="execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
        },
        timeout=20.0,
    ).json()

    if "error" in response:
        raise APIError(response["error"]["error_msg"])

    response = list(chain.from_iterable(response["response"]))
    return response


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """

    def get_wall_info(code: str):
        response = session.post(
            url="execute",
            data={
                "code": code,
                "access_token": config.VK_CONFIG["access_token"],
                "v": config.VK_CONFIG["version"],
            },
            timeout=20.0,
        ).json()
        if "error" in response:
            raise APIError(response["error"]["error_msg"])
        else:
            return response["response"]

    total_count = get_wall_info(
        f"""var docs=API.wall.get({{"domain":"{domain}","count":"{count}"}});return docs.count;"""
    )
    time.sleep(1)
    if count == 0:
        count = total_count
    elif count <= 100:
        code = f"""var docs=API.wall.get({{"owner_id":"{owner_id}","extended":"{extended}","domain":"{domain}","count":"{count}","offset":"{offset}","filter":"{filter}"}});return docs;"""
        return json_normalize(get_wall_info(code)["items"])

    if count % max_count == 0:
        count_of_iter = count // max_count
    else:
        count_of_iter = count // max_count + 1

    posts = []
    with tqdm(total=count, disable=False if progress else True) as pbar:
        for i in range(0, count_of_iter):
            offset = offset + max_count * i
            response = get_posts_2500(
                count=count,
                owner_id=owner_id,
                domain=domain,
                offset=offset,
                max_count=max_count,
                filter=filter,
                extended=extended,
            )
            count = count - max_count

            for j in response:
                posts.append(j)
                pbar.update(1)

            if count_of_iter > 1:
                time.sleep(1 / 3)

    pbar.close()
    return json_normalize(posts)
