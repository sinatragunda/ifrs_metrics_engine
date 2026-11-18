# Created by Sinatra Gunda 
# Created at 17/11/2026 07:54
# Kindly contact me at @sinatragunda or treyviis@gmail.com

from .apps import IfrsBootInfrastuctureApp
from . import constants

__all__  =["middleware", "wire_container" ,"IfrsBootInfrastuctureApp" ,"constants"]

def __getattr__(name):

    if name == "middleware":
        from . import middleware
        return middleware

    if name in ("Container", "wire_container"):
        from .container_bean import Container, wire_container

        return {
            "Container": Container,
            "wire_container": wire_container
        }[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")