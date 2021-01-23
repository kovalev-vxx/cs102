import datetime as dt
import time
import typing as tp
from statistics import median

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    request = get_friends(user_id=user_id, fields=["bdate"])
    curret_year = int(dt.datetime.now().year)
    friends_age = []

    for i in list(request.items):
        bdate = str(i.get("bdate"))  # type: ignore
        if bdate != None:
            bdate = str(bdate[-4:])  # type: ignore
            try:
                birth_years = int(time.strptime(bdate, "%Y").tm_year)
                friends_age.append(curret_year - birth_years)
            except (ValueError):
                pass
    if len(friends_age) == 0:
        return None
    else:
        predict = median(sorted(friends_age))
        return predict
