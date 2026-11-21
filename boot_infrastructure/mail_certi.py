# Created by Sinatra Gunda 
# Created at 21/11/2026 18:33
# Kindly contact me at @sinatragunda or treyviis@gmail.com

# myapp/email_backend.py
import ssl
import certifi
from functools import cached_property
from django.core.mail.backends.smtp import EmailBackend

class CertifiEmailBackend(EmailBackend):
    @cached_property
    def ssl_context(self):
        return ssl.create_default_context(cafile=certifi.where())