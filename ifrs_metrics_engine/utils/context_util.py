# Created by Sinatra Gunda 
# Created at 18/11/2026 09:15
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import hashlib
import os
import uuid

from pathlib import Path


from boot_infrastructure.context.user_session_context import user_session_context_var, UserSession
from boot_infrastructure.exceptions.custom_exceptions import NotAuthenticated, NotAuthenticatedWithLoginRequirement


def get_clerk_secret_key():
    return os.environ.get("CLERK_SECRET_KEY")

def get_session_user(throws = True)-> UserSession:
    user_data = user_session_context_var.get()
    if not user_data:
        raise Exception("No user data found")
    if not user_data.user_model and throws:
        raise NotAuthenticatedWithLoginRequirement("User session expired or not authenticated")

    return user_data


def generate_model_id(key):
    return f'{key}{uuid.uuid4().hex}'

def get_resources_folder():
    print(__file__)
    base_dir = Path(__file__).resolve().parent
    print(base_dir)
    return f'{base_dir}\\resources'
