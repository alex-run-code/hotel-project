from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Listing, HotelRoom, BlockedDay, BookingInfo
from .serializers import ListingSerializer
from django.db.models import Min
from django.db.models import CharField, Value, IntegerField


# Create your views here.

class UnitList(ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_queryset(self):
        check_in = '2021-04-25'
        check_out = '2021-04-30'

        available_hotel_rooms = HotelRoom.objects\
            .exclude(blocked_day_hr__date__range=[check_in, check_out])\
                .prefetch_related('hotel_room_type__hotel')

        apts = Listing.objects\
            .exclude(blocked_day_listing__date__range=[check_in, check_out])\
            .filter(listing_type='apartment')\
            .annotate(price=Min('booking_info__price'))

        hotels = Listing.objects\
            .filter(hotel_room_types__hotel_rooms__in=available_hotel_rooms)\
            .filter(listing_type='hotel')\
            .annotate(price=Min('hotel_room_types__booking_info__price'))
        
        units = apts.union(hotels)
        return(units)

