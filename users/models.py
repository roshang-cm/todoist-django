from django.db import models
from django.contrib.auth.models import AbstractUser

ACCOUNT_STATUSES = (('active', 'Active'), ('blocked', 'Blocked'))


class User(AbstractUser):
    account_status = models.CharField(
        max_length=20, choices=ACCOUNT_STATUSES, default='active')
