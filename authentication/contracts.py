from django.db import models


class UserTypes(models.TextChoices):
    MANAGER = 'manager', 'Manager'
    APPLICANT = 'applicant', 'Applicant'
