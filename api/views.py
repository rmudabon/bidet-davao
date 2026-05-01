from locations.models import Location
from locations.serializers import LocationSerializer, PresignedUploadSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from locations.utils.s3 import S3

# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view locations
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Location.objects.all().order_by("-created_at")
    serializer_class = LocationSerializer
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