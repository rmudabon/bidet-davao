from locations.models import Location
from locations.serializers import LocationSerializer
from rest_framework import viewsets

# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view locations
    """

    queryset = Location.objects.all().order_by("-created_at")
    serializer_class = LocationSerializer
