import factory
from django.contrib.auth import get_user_model

from restaurant_service.models import Restaurant, Menu


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall(
        'set_password',
        'defaultpassword'
    )
    is_owner = factory.Faker("pybool")
    is_superuser = factory.Faker("pybool")


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.Faker('company')
    date_added = factory.Faker('date_time_this_decade', before_now=True, after_now=False, tzinfo=None)
    address = factory.Faker('address')
    contact_number = factory.Faker('phone_number')
    contact_email = factory.Faker('email')
    description = factory.Faker('paragraph')
    website = factory.Faker('url')
    capacity = factory.Faker('random_int', min=10, max=200)
    cuisine_type = factory.Faker('word')

    owner = factory.SubFactory(UserFactory)
