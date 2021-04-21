from datetime import datetime

from .user_regiter import register, login, check
from .brands_init import brands_init
# from .brands import add, get, get_all
from .disease_init import diseases_init


def today():
    return datetime.today()