import factory
from authentication.models import User
from authentication.contracts import UserTypes


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username %d' % n)
    first_name = 'John'
    last_name = 'Doe'
    email = 'email@email.com'
    type = UserTypes.APPLICANT
    phone = '+33123456789'