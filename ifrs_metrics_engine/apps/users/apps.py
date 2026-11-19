import os

from clerk_backend_api import Clerk, Users
from dependency_injector.wiring import Provide, inject
from django.apps import AppConfig

from boot_infrastructure.container_bean import Container
from ifrs_metrics_engine.apps.users.user_service import UserService


class UsersConfig(AppConfig):

    name = "ifrs_metrics_engine.apps.users"

    @inject
    def ready(self ,user_service : UserService = Provide[Container.user_service] ):

        clerk_key = os.environ['CLERK_KEY']

        clerk = Clerk(bearer_auth=clerk_key)
        users = clerk.users.list()

        if len(users) > 0:
            for clerk_user in users:
                user = user_service.find_user_by_auth_id(auth_id=clerk_user.id)
                if not user:
                    user_service.create_user(user=clerk_user)




