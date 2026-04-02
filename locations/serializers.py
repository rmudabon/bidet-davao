from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import Location
class LocationSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, min_value=-90, max_value=90, write_only=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, min_value=-180, max_value=180, write_only=True)

    lat = serializers.SerializerMethodField(read_only=True)
    lng = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Location
        fields = ["id", "name", "address", "latitude", "longitude", "stall_type", "description", "image_url", 'lat', 'lng']

    def create(self, validated_data):
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        validated_data['point'] = Point((longitude, latitude))

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'latitude' in validated_data and 'longitude' in validated_data:
            latitude = validated_data.pop('latitude')
            longitude = validated_data.pop('longitude')
            instance.point = Point((longitude, latitude))

        return super().update(instance, validated_data)
    
    # Points are stored in (long, lat) as of PostGIS
    def get_lat(self, obj):
        return obj.point.y if obj.point else None

    def get_lng(self, obj):
        return obj.point.x if obj.point else None

class PresignedUploadSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_type = serializers.CharField()
    