from locations.serializers import PresignedUploadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class UploadView(APIView):
    permission_classes = [IsAuthenticated]
    