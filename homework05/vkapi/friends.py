import dataclasses
import math
import time
import typing as tp

import requests
from tqdm import tqdm

from vkapi import config, session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """

    params = {
        "access_token": config.VK_CONFIG["access_token"],
        "v": config.VK_CONFIG["version"],
        "user_id": user_id,
        "fields": fields,
        "count": count,
        "offset": offset,
    }

    response = session.get(url="friends.get", params=params)
    doc = response.json()

    if "error" in doc or not response.ok:
        raise APIError(doc["error"]["error_msg"])

    return FriendsResponse(**doc["response"])  # type: ignore


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    if target_uids:

        count_of_iter = (len(target_uids) + 99) // 100

        response_info = []

        with tqdm(total=count_of_iter, disable=True if progress is None else False) as pbar:
            for i in range(0, count_of_iter):

                params = {
                    "access_token": config.VK_CONFIG["access_token"],
                    "source_uid": source_uid if source_uid is not None else "",
                    "v": config.VK_CONFIG["version"],
                    "target_uids": str(target_uids)[1:-1],
                    "order": order,
                    "count": count if count is not None else "",
                    "offset": offset + i * 100,
                }

                response = session.get(url="friends.getMutual", params=params)
                doc = response.json()

                if "error" in response or not response.ok:  # type: ignore
                    raise APIError(doc["error"]["error_msg"])  # type: ignore

                pbar.update(1)

                if count_of_iter > 1:
                    time.sleep(1 / 3)

                for arg in doc["response"]:
                    response_info.append(MutualFriends(arg))  # type: ignore
            pbar.close()
    else:

        params = {
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
            "source_uid": source_uid if source_uid is not None else "",
            "target_uid": target_uid,
            "order": order,
            "count": count if count is not None else "",
            "offset": offset,
        }

        response = session.get(url="friends.getMutual", params=params)
        response_info = response.json()

        if "error" in response_info or not response.ok:
            raise APIError(response_info["error"]["error_msg"])  # type: ignore

        return response_info["response"]  # type: ignore

    return response_info
