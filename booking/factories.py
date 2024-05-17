import factory
from django.utils.crypto import get_random_string

from .models import User, Room, Booking, Payment, Service, BookingService, Discount, Review
from factory import fuzzy
from django.utils import timezone



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    surname = factory.Faker('last_name')
    name = factory.Faker('first_name')
    email = factory.Sequence(lambda n: f"{get_random_string(8)}@example.com")
    password = factory.Faker('password')
    phone = factory.Faker('phone_number')

class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    room_number = factory.Sequence(lambda n: f"Room {n}")
    room_type = factory.Faker('word')
    price = fuzzy.FuzzyDecimal(50, 300)
    availability = factory.Faker('boolean')

class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    booking_date = factory.Faker('date_time')
    check_in_date = factory.Faker('date_time')
    check_out_date = factory.Faker('date_time')
    user = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def room(self):
        return Room.objects.order_by('?').first()
class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    amount = fuzzy.FuzzyDecimal(10, 500)
    date = factory.Faker('date_time')
    payment_method = factory.Faker('credit_card_provider')
    booking = factory.SubFactory(BookingFactory)

class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    name = factory.Faker('word')
    description = factory.Faker('text')
    price = fuzzy.FuzzyDecimal(5, 50)

class BookingServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookingService

    booking = factory.SubFactory(BookingFactory)
    service = factory.SubFactory(ServiceFactory)
    quantity = factory.Faker('random_digit')
    date_time = factory.Faker('date_time')

class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount

    name = factory.Faker('word')
    description = factory.Faker('text')
    percentage = fuzzy.FuzzyFloat(0, 100)

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    rating = fuzzy.FuzzyFloat(0, 5)
    user = factory.SubFactory(UserFactory)
    booking = factory.SubFactory(BookingFactory)
