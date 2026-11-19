# Created by Sinatra Gunda 
# Created at 19/11/2026 13:13
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from functools import wraps

from django.db import transaction


def atomic_op(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        with transaction.atomic():
            return func(*args,**kwargs)
    return wrapper
