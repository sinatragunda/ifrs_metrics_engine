
from .apps import UsersConfig

__all__ = ['UsersConfig',"Users"]

def __getattr__(name):

    if name == "Users":
        from . import Users
        return Users

    raise AttributeError(name)