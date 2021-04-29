import factory
from .models import HotelRoom, HotelRoomType, Listing, BlockedDay, BookingInfo
from datetime import date
import random

class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listing

    listing_type = 'apartment'
    title = factory.Sequence(lambda n: 'Listing%d' % n)
    country = factory.Sequence(lambda n: 'Country%d' % n)
    city = factory.Sequence(lambda n: 'City%d' % n)

class HotelRoomTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelRoomType

    hotel = factory.SubFactory(ListingFactory)
    title = factory.Sequence(lambda n: 'hotelroomtype%d' % n)

class HotelRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HotelRoom

    hotel_room_type = factory.SubFactory(HotelRoomTypeFactory),
    room_number = factory.Sequence(lambda n: 'hotelroom%d' % n)

class BlockedDayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlockedDay

    date = date.today
    listing = None
    hotel_room = None


class BookingInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookingInfo
    
    listing = factory.SubFactory(ListingFactory)
    hotel_room_type = factory.SubFactory(HotelRoomTypeFactory)
    price = factory.LazyAttribute(random.randrange(20, 250))