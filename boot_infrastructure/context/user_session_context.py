# Created by Sinatra Gunda 
# Created at 18/11/2026 04:02
# Kindly contact me at @sinatragunda or treyviis@gmail.com

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Optional

from ifrs_metrics_engine.apps.users.models import Users


@dataclass
class UserSession:
    auth_user_id : str
    firstname : str
    lastname : str
    username : str
    email : str
    user_model : Optional[Users] = None

user_session_context_var : ContextVar[UserSession]  = ContextVar("user_details" ,default = None)
