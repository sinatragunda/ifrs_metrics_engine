# Created by Sinatra Gunda 
# Created at 18/11/2026 09:12
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from rest_framework.exceptions import NotFound

from ifrs_metrics_engine.apps.users.models import Users
from ifrs_metrics_engine.utils.context_util import get_session_user


class UserService:

    def find_user_by_email(self,email):
        pass

    def create_user(self ,user):
        pass

    def find_user_by_auth_id(self,auth_id ,create_when_not_found=False):
        user = Users.objects.filter(auth_user_id=auth_id).first()
        if not user:
            if create_when_not_found:
                user_session = get_session_user()
                user_model = Users(auth_user_id=auth_id,username = user_session.username, display_name=f'{user_session.firstname} {user_session.lastname}',email=user_session.email)
                return user_model.save()
            raise NotFound("User Not Found")

        return user