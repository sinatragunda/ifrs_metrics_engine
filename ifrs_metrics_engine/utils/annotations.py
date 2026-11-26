# Created by Sinatra Gunda 
# Created at 19/11/2026 13:13
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from functools import wraps

from django.db import transaction, IntegrityError

from boot_infrastructure.exceptions.custom_exceptions import ConflictError


def atomic_op(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        with transaction.atomic():
            try:
                return func(*args,**kwargs)
            except IntegrityError as e:
                raise ConflictError(f'Record already exists {e.__str__()}')
    return wrapper
