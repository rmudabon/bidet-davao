from .models import Location
from rest_framework import serializers

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ["name", "address", "latitude", "longitude", "description", "image_url"]