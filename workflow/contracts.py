from django.db import models


class JobContracts(models.TextChoices):
    PERMANENT = 'permanent', 'Permanent Contract'
    FIXED = 'fixed', 'Fixed-Time Contract'
    INTERNSHIP = 'internship', 'Internship'


class JobTypes(models.TextChoices):
    FULL_TIME = 'full_time', 'Full-Time'
    PART_TIME = 'part_time', 'Part-Time'


class JobModalities(models.TextChoices):
    REMOTE = 'remote', 'Remote'
    ON_SITE = 'on_site', 'On site'
    HYBRID = 'hybrid', 'Hybrid'


class ApplicationStatuses(models.TextChoices):
    APPLIED = 'applied', 'Applied'
    IN_REVIEW = 'in_review', 'In review'
    WAITING_FOR_ITW = 'waiting', 'Waiting for interview'
    OFFER = 'offer', 'Offer'
    DISQUALIFIED = 'disqualified', 'Disqualified'
