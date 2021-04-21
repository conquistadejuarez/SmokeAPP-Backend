from datetime import datetime

from .user_regiter import register, login, check
from .brands_init import brands_init
# from .brands import add, get, get_all
from .disease_init import diseases_init

import users_models as models
import uuid

def today():
    return datetime.today()


async def days_since_user_quits(id_user: uuid.UUID):
    user = await models.User.filter(id=id_user).get_or_none()

    if not user:
        return {'status': 'error', 'id_error': 'USER_NOT_FOUND'}

    return user.days_since_user_quits
