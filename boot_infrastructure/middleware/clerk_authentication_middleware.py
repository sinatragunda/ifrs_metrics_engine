# Created by Sinatra Gunda 
# Created at 18/11/2026 00:19
# Kindly contact me at @sinatragunda or treyviis@gmail.com


import os
import re

from clerk_backend_api import Clerk, AuthenticateRequestOptions
from dependency_injector.wiring import Provide, inject
from rest_framework.exceptions import NotAuthenticated
from django.conf import settings

from boot_infrastructure.context.user_session_context import user_session_context_var, UserSession
from ifrs_metrics_engine.apps.users.user_service import UserService

CLERK_SECRET_KEY   = os.environ.get('CLERK_SECRET_KEY') # if null we need to stop app and return internal server
EXEMPT_URLS = getattr(settings, 'AUTH_EXEMPT_URIS', [])

class ClerkAuthenticationMiddleware:

    @inject
    def __init__(self ,get_response ,user_service : UserService = Provide['user_service']):
        self.get_response = get_response
        self.user_service = user_service

    def __call__(self, request):

        user_service = self.user_service

        if self.is_exempt(request):
            return self.get_response(request)

        bearer_token = request.headers.get('Authorization')

        if bearer_token:

            clerk = Clerk(bearer_auth = CLERK_SECRET_KEY)

            if clerk:
                request_state = clerk.authenticate_request(request ,AuthenticateRequestOptions())

                #print(f" we have request {request_state}")
                #print(f"token state {request_state.is_authenticated} and {request_state.is_signed_in}")
                if request_state.is_authenticated:
                    #print(request_state)

                    user_id = request_state.payload['sub']

                    with Clerk(bearer_auth = CLERK_SECRET_KEY) as client_clerk:

                        user_data = client_clerk.users.get(user_id = user_id)
                        request.client_data = user_data
                        user_entity = user_service.find_user_by_auth_id(user_id)

                        user_session = {
                            'auth_user_id':user_data.id,
                            'username': user_data.username,
                            'firstname': user_data.first_name,
                            'lastname': user_data.last_name,
                            'email': user_data.email_addresses[0].email_address,
                            'user_model': user_entity,
                        }

                        print("does authentication happen here often ? ",user_entity)

                        user_session = UserSession(**user_session)
                        user_session_context_var.set(user_session)

                    return self.get_response(request)

        raise NotAuthenticated()

    def is_exempt(self ,request):

        if request.method == "OPTIONS":
            return True

        print(EXEMPT_URLS)

        path = request.path_info.lstrip("/")

        if any(re.match(pattern, path) for pattern in EXEMPT_URLS):
            return True

        return False