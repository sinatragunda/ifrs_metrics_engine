# Created by Sinatra Gunda 
# Created at 18/11/2026 09:12
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import os

from clerk_backend_api import Clerk, models
from django.apps import apps
from rest_framework.exceptions import NotFound
from starlette.status import HTTP_400_BAD_REQUEST

from boot_infrastructure.exceptions.custom_exceptions import InternalServerError
from ifrs_metrics_engine.apps.users.models import Users
from ifrs_metrics_engine.utils.context_util import get_session_user


class UserService:

    def find_user_by_email(self,email):
        pass

    def create_user(self ,user):
        if not user:
            raise HTTP_400_BAD_REQUEST
        return user.save()


    def clerk_create_user(self ,email):

       clerk: Clerk  = Clerk(bearer_auth=os.getenv('CLERK_SECRET_KEY'))
       if not clerk:
           raise HTTP_400_BAD_REQUEST

       try:
         user_request = {
             'email_address': [email],
         }
         user_record = clerk.users.list(request=user_request)
         if not user_record:
             raise NotFound("User Not Found")
         clerk_user = user_record[0]
         return self.find_user_by_auth_id(clerk_user.id ,create_when_not_found=True)

       except:
           # email not found lets create new record
           print("email id is  ",email)
           user_data = {
               'email_address': [email],
               'username': email,
               'skip_password_requirement':True
           }
           try:
               return True
                #clerk_user =  clerk.users.create(**user_data)
                #print("User Created Successfully" ,clerk_user.__str__())
                #user_model = Users(auth_user_id = clerk_user.id , email = email ,username = email)
                #return user_model.save()
           except Exception as e:
               print(e)
               raise InternalServerError(e.__str__())

    def find_user_by_auth_id(self,auth_id ,create_when_not_found=False):
        #Users = apps.get_model('users', 'Users')
        user = Users.objects.filter(auth_user_id=auth_id).first()
        if not user:
            if create_when_not_found:
                user_session = get_session_user()
                user_model = Users(auth_user_id=auth_id,username = user_session.username, display_name=f'{user_session.firstname} {user_session.lastname}',email=user_session.email)
                return self.create_user(user_model)
            raise NotFound("User Not Found")

        return user