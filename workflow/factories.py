import factory
import datetime
from workflow import models
from authentication.factories import UserFactory


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    jobs = factory.RelatedFactoryList(
        'workflow.factories.JobFactory',
        factory_related_name='company',
        size=1
    )
    name = 'Company'
    created_at = datetime.datetime.now()


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Job

    applications = factory.RelatedFactoryList(
        'workflow.factories.ApplicationFactory',
        factory_related_name='job',
        size=1
    )
    company = factory.SubFactory(CompanyFactory)
    title = factory.Sequence(lambda n: 'job %d' % n)
    category = 'Engineering'
    created_at = datetime.datetime.now()


class ApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Application

    applicant = factory.SubFactory(UserFactory)
    job = factory.SubFactory(JobFactory)
    created_at = datetime.datetime.now()
