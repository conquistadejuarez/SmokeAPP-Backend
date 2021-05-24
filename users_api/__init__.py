from datetime import datetime

from .user_regiter import register, login, check
from .brands_init import brands_init
# from .brands import add, get, get_all
from .disease_init import diseases_init

import users_models as models
import uuid


def today():
    return datetime.today()


async def __str__(id_user: uuid.UUID):
    user = await models.User.filter(id=id_user).get_or_none()

    if not user:
        return {'status': 'error', 'id_error': 'USER_NOT_FOUND'}

    return user.__str__()


async def days_since_user_quits(id_user: uuid.UUID):
    user = await models.User.filter(id=id_user).get_or_none()

    if not user:
        return {'status': 'error', 'id_error': 'USER_NOT_FOUND'}

    if user.days_since_user_quits > 0:
        return user.days_since_user_quits

    return 0


async def calc_money_spend_per_day(id_user: uuid.UUID):
    user = await models.User.filter(id=id_user).get_or_none()

    if not user:
        return {'status': 'error', 'id_error': 'USER_NOT_FOUND'}

    if await user.calc_money_spend_per_day() > 0:
        return await user.calc_money_spend_per_day()
    return 0


async def calc_money_not_spend(id_user: uuid.UUID):
    user = await models.User.filter(id=id_user).get_or_none()

    if not user:
        return {'status': 'error', 'id_error': 'USER_NOT_FOUND'}

    if await user.calc_money_not_spend() > 0:
        return await user.calc_money_not_spend()
    return 0


async def calc_cigarettes_user_did_not_smoke(id_user):
    user = await models.User.filter(id=id_user).get_or_none()

    if not user:
        return {'status': 'error', 'id_error': 'USER_NOT_FOUND'}
    if user.calc_cigarettes_user_did_not_smoke() > 0:
        return user.calc_cigarettes_user_did_not_smoke()
    return 0
