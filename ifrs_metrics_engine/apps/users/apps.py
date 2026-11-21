import os
from typing import TYPE_CHECKING

from clerk_backend_api import Clerk
from dependency_injector.wiring import Provide, inject
from django.apps import AppConfig
from rest_framework.exceptions import NotFound




class UsersConfig(AppConfig):

    name = "ifrs_metrics_engine.apps.users"

    def ready(self):

        from boot_infrastructure.container_bean import Container
        user_service = Container.user_service()
        clerk_key = os.environ['CLERK_SECRET_KEY']

        clerk = Clerk(bearer_auth=clerk_key)
        users = clerk.users.list()

        if len(users) > 0:
            for clerk_user in users:
                try:
                    user_service.find_user_by_auth_id(auth_id=clerk_user.id)
                except Exception as e:
                    print(type(e))
                    if type(e) == NotFound:
                        print("Create user with details " ,clerk_user)
                        from ifrs_metrics_engine.apps.users.models import Users
                        display_name = f'{clerk_user.first_name} {clerk_user.last_name}'
                        email = f'{clerk_user.primary_email_address_id}'
                        user = Users(auth_user_id=clerk_user.id ,display_name=display_name ,username=clerk_user.username)
                        user_service.create_user(user)




