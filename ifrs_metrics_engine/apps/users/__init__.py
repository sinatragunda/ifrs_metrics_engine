

import importlib

# def __getattr__(name):
#
#     if name == "Users":
#         models = importlib.import_module(".models" ,__name__)
#         return models.Users
#
#     if name == "UsersConfig":
#         from .apps import UsersConfig
#         return UsersConfig
#
#     raise AttributeError(name)