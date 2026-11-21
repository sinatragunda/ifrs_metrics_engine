# Created by Sinatra Gunda 
# Created at 18/11/2026 09:15
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import os

from pathlib import Path
from boot_infrastructure.context.user_session_context import user_session_context_var
from boot_infrastructure.middleware.clerk_authentication_middleware import CLERK_SECRET_KEY

CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")

def get_clerk_secret_key():
    return CLERK_SECRET_KEY

def get_session_user():
    user_data = user_session_context_var.get()
    if not user_data:
        raise Exception("No user data found")
    return user_data


def get_resources_folder():

    base_dir = Path(__file__).resolve().parent
    print(base_dir)
    return f'{base_dir}/resources'
