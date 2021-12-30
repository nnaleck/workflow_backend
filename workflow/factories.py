import factory
import datetime
from workflow import models
from workflow.contracts import UserTypes
from faker import Faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'username %d' % n)
    first_name = 'John'
    last_name = 'Doe'
    email = 'email@email.com'
    type = UserTypes.APPLICANT
    phone = '+33123456789'


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    jobs = factory.RelatedFactoryList(
        'workflow.factories.JobFactory',
        factory_related_name='company',
        size=1
    )
    name = Faker().company
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