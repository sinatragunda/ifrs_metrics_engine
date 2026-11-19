# Created by Sinatra Gunda 
# Created at 19/11/2026 09:50
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import os
from dataclasses import dataclass, field

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

MAIL_SENDER = os.environ.get('MAIL_SENDER')

@dataclass
class EmailDetails:
    email: str
    subject: str
    body: str
    attachments: list = field(default_factory=list)
    cc: list[str] = field(default_factory=list)
    bcc: list[str] = field(default_factory=list)
    template: str | None = None
    kwargs: dict = field(default_factory=dict)

class EmailService:

    def send_email(self, email_details: EmailDetails):

        if email_details.template:
            html_content = render_to_string(email_details.template, email_details.kwargs)
            msg = EmailMultiAlternatives(to=email_details.email,subject= email_details.subject,from_email=MAIL_SENDER ,bcc=email_details.bcc ,cc=email_details.bcc)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            send_mail(email_details.email,email_details.subject,MAIL_SENDER ,[email_details.email],fail_silently=False)

