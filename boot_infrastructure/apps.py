# Created by Sinatra Gunda 
# Created at 18/11/2026 01:04
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.apps import AppConfig

class IfrsBootInfrastuctureApp(AppConfig):
    name = "boot_infrastructure"

    def ready(self):
        print("App ready wire container ")
        from boot_infrastructure import wire_container
        wire_container()