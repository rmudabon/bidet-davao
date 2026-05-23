from locations.models import Location
from locations.serializers import LocationSerializer, PresignedUploadSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from locations.utils.s3 import S3
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.shortcuts import get_object_or_404

# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view locations
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Location.objects.all().order_by("-created_at")
    serializer_class = LocationSerializer

    def get_queryset(self):
        qs = Location.objects.filter(status=Location.Status.ACTIVE)

        is_mine = self.request.query_params.get("mine", "").lower() == "true"
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")
        radius = int(self.request.query_params.get("radius", 50)) # In meters

        if is_mine and self.request.user.is_authenticated:
            qs = Location.objects.filter(created_by=self.request.user)
            return qs

        if lat and lng:
            user_point = Point(float(lng), float(lat), srid=4326)  # Note: Point takes (longitude, latitude)
            qs = (
                qs
                .filter(point__distance_lte=(user_point, D(m=radius)))
                .annotate(distance=Distance('point', user_point))
                .order_by('distance')
            )
        

        return qs
    
    def get_object(self):
        obj = get_object_or_404(Location, pk=self.kwargs['pk'])

        if obj.status != Location.Status.ACTIVE: 
            if not self.request.user.is_authenticated or obj.created_by != self.request.user:
                raise PermissionDenied("You do not have permission to access this location.")
        
        self.check_object_permissions(self.request, obj)
        return obj



class UploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PresignedUploadSerializer(data=request.data)
        if serializer.is_valid():
            s3 = S3()
            file_name = serializer.validated_data['file_name']
            presigned_url = s3.generate_upload_url(file_name)
            if presigned_url:
                return Response({"url": presigned_url}, status=status.HTTP_200_OK)
            return Response({"detail": "Failed to generate presigned URL."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)