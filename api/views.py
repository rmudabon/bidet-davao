from django.contrib.auth import authenticate, logout, login

from locations.models import Location
from locations.serializers import LocationSerializer, PresignedUploadSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.views import APIView

# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view locations
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Location.objects.all().order_by("-created_at")
    serializer_class = LocationSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Credentials are invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
        
        logout(request)
        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
    
class UploadView(APIView):
    permission_classes = [IsAuthenticated]
   