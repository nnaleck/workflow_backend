from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.contracts import UserTypes


# User model
class User(AbstractUser):
    type = models.CharField(
        max_length=20,
        choices=UserTypes.choices,
        default=UserTypes.APPLICANT
    )

    phone = models.CharField(max_length=12)
