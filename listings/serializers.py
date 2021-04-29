from .models import Listing
from rest_framework import serializers

class ListingSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()
    
    class Meta:
        model = Listing
        fields = '__all__'