from django.db import models
from django.contrib.auth.models import AbstractUser
from workflow.contracts import UserTypes, JobTypes, JobContracts, JobModalities, ApplicationStatuses


# User model
class User(AbstractUser):
    type = models.CharField(
        max_length=20,
        choices=UserTypes.choices,
        default=UserTypes.APPLICANT
    )

    phone = models.CharField(max_length=12)


# Company model
class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Job model
class Job(models.Model):
    company = models.ForeignKey(
        'Company',
        related_name='jobs',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField(null=True)

    contract = models.CharField(
        max_length=30,
        choices=JobContracts.choices,
        default=JobContracts.PERMANENT
    )

    type = models.CharField(
        max_length=30,
        choices=JobTypes.choices,
        default=JobTypes.FULL_TIME
    )

    modalities = models.CharField(
        max_length=30,
        choices=JobModalities.choices,
        default=JobModalities.HYBRID
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(default=None, blank=True, null=True)
    closed_at = models.DateTimeField(default=None, blank=True, null=True)


# Application model
class Application(models.Model):
    applicant = models.ForeignKey(
        'User',
        related_name='applications',
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        'Job',
        related_name='applications',
        on_delete=models.CASCADE
    )

    description = models.TextField(null=True)
    attachments = models.JSONField(null=True)
    status = models.CharField(
        max_length=30,
        choices=ApplicationStatuses.choices,
        default=ApplicationStatuses.APPLIED
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
