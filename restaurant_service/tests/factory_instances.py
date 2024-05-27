import factory
from django.contrib.auth import get_user_model

from polling_service.models import Poll
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


class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poll

    created_at = factory.Faker('date')
    is_closed = factory.Faker('boolean')


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    name = factory.Faker('word')
    date_added = factory.Faker('date')
    menu_file = factory.django.FileField(filename='menu.pdf')
    restaurant = factory.SubFactory(RestaurantFactory)
    poll = factory.SubFactory(PollFactory)

