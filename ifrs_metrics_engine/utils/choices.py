# Created by Sinatra Gunda
# Created at 19/11/2026 08:31
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from enum import Enum

from django.db import models


class ACCESS_SCOPES(models.TextChoices):
    ALL = 'all'
    READ = 'read'
    WRITE = 'write'
    READ_WRITE = 'read_write'


class IFRS_STANDARD(models.TextChoices):
    IFRS_9 = "ifrs_9", "IFRS 9"
    IFRS_15 = "ifrs_15", "IFRS 15"
    IFRS_16 = "ifrs_16", "IFRS 16"
    IFRS_17 = "ifrs_17", "IFRS 17"


class INVITATION_STATUS(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    EXPIRED = "expired", "Expired"
    REVOKED = "revoked", "Revoked"