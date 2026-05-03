from django.contrib.auth import authenticate, login, logout

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import RegisterSerializer, UserSerializer

# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
        
        logout(request)
        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
    
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    