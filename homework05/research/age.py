import datetime as dt
import time
import typing as tp
from statistics import median

from vkapi.friends import get_friends  # type: ignore


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    request = get_friends(user_id=user_id, fields="bdate")
    curret_year = int(dt.datetime.now().year)
    friendsAge = []

    for i in request.items:
        bdate = i.get("bdate")
        if bdate != None:
            bdate = bdate[-4:]
            try:
                birthYears = int(time.strptime(bdate, "%Y").tm_year)
                friendsAge.append(curret_year - birthYears)
            except (ValueError):
                pass
    if len(friendsAge) == 0:
        return None
    else:
        predict = median(sorted(friendsAge))
        return predict
