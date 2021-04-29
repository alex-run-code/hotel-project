from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Listing
from .factories import BlockedDayFactory, HotelRoomTypeFactory, HotelRoomFactory, ListingFactory, BookingInfoFactory
import datetime
from django.core import serializers
from .serializers import ListingSerializer



# Create your tests here.

class BookingTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.hotel_lux = ListingFactory(title='hotel lux', listing_type='hotel')
        self.apartment = ListingFactory(title='apartment', listing_type='apartment')

        self.hotelroomdouble = HotelRoomTypeFactory(hotel=self.hotel_lux, title='double room')
        self.hotelroomtriple = HotelRoomTypeFactory(hotel=self.hotel_lux, title='triple room')
        self.hotelroomsuite = HotelRoomTypeFactory(hotel=self.hotel_lux, title='suite')

        self.hotelroom121 = HotelRoomFactory(hotel_room_type=self.hotelroomdouble)
        self.hotelroom122 = HotelRoomFactory(hotel_room_type=self.hotelroomdouble)
        self.hotelroom131 = HotelRoomFactory(hotel_room_type=self.hotelroomtriple)
        self.hotelroom141 = HotelRoomFactory(hotel_room_type=self.hotelroomsuite)

        self.bookinginfo_doubleroom = BookingInfoFactory(listing=None, hotel_room_type=self.hotelroomdouble, price='50')
        self.bookinginfo_tripleroom = BookingInfoFactory(listing=None, hotel_room_type=self.hotelroomtriple, price='60')
        self.bookinginfo_suite = BookingInfoFactory(listing=None, hotel_room_type=self.hotelroomsuite, price='200')
        self.bookinginfo_apt = BookingInfoFactory(listing=self.apartment, hotel_room_type=None, price='250')
        
    def test_all_is_available(self):
        """ everything should be displayed """
        params = {
            'max_price':'800',
            'check_in':'2021-04-27',
            'check_out':'2021-04-29'
        }

        response = self.client.get(reverse('units'), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], self.hotel_lux.title)
        self.assertEqual(response.data[1]['title'], self.apartment.title)

    def test_booking_hotel_fully_booked(self):
        """ hotel_lux should not be displayed """
        blocked_day_room121 = BlockedDayFactory(date=datetime.datetime(2021, 4, 28), hotel_room=self.hotelroom121)
        blocked_day_room122 = BlockedDayFactory(date=datetime.datetime(2021, 4, 28), hotel_room=self.hotelroom122)
        blocked_day_room131 = BlockedDayFactory(date=datetime.datetime(2021, 4, 28), hotel_room=self.hotelroom131)
        blocked_day_room141 = BlockedDayFactory(date=datetime.datetime(2021, 4, 28), hotel_room=self.hotelroom141)
        
        params = {
            'max_price':'800',
            'check_in':'2021-04-27',
            'check_out':'2021-04-29'
        }

        serializer = ListingSerializer(Listing.objects.all(), many=True)
        response = self.client.get(reverse('units'), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], self.apartment.title)

    def test_some_rooms_are_booked_but_all_room_type_are_available(self):
        """ 
        Some rooms are booked, but all room types are still available
        """
        blocked_day_room121 = BlockedDayFactory(date=datetime.datetime(2021, 4, 28), hotel_room=self.hotelroom121)
        
        params = {
            'max_price':'800',
            'check_in':'2021-04-27',
            'check_out':'2021-04-29'
        }

        response = self.client.get(reverse('units'), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], self.hotel_lux.title)
        self.assertEqual(response.data[1]['title'], self.apartment.title)

    def test_all_doublerooms_are_booked(self):
        """ 
        All double rooms are booked, so the price displayed 
        should be the one of a triple room
        """
        blocked_day_room121 = BlockedDayFactory(date=datetime.datetime(2021, 4, 28), hotel_room=self.hotelroom121)
        blocked_day_room122 = BlockedDayFactory(date=datetime.datetime(2021, 4, 28), hotel_room=self.hotelroom122)
        
        params = {
            'max_price':'800',
            'check_in':'2021-04-27',
            'check_out':'2021-04-29'
        }

        response = self.client.get(reverse('units'), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['price'], float(self.bookinginfo_tripleroom.price))
        self.assertEqual(response.data[1]['price'], float(self.bookinginfo_apt.price))

    def test_apartments_sorted_by_price(self):
        """ 
        Apartments are sorted by price, from the lowest price to
        the highest price
        """
        print(Listing.objects.all())
        self.hotel_lux.delete()
        apartment2 = ListingFactory(title='apartment2', listing_type='apartment')
        bookinginfo_apt2 = BookingInfoFactory(listing=apartment2, price='260')
        
        params = {
            'max_price':'800',
            'check_in':'2021-04-27',
            'check_out':'2021-04-29'
        }
        response = self.client.get(reverse('units'), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], self.apartment.title)
        self.assertEqual(response.data[1]['title'], apartment2.title)

    def test_above_max_price_units_not_displayed(self):
        """ 
        Units above the max_price are not displayed
        """
        params = {
            'max_price':'80',
            'check_in':'2021-04-27',
            'check_out':'2021-04-29'
        }

        response = self.client.get(reverse('units'), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], self.hotel_lux.title)
