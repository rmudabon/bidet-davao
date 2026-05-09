import openrouteservice
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class GeoAutoCompleteView(APIView):
    client = openrouteservice.Client(key=settings.ORS_API_KEY)

    def get(self, request):
        search_text = request.query_params.get('text')
        if not search_text:
            return Response({"error": "Missing 'text' query parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            results = self.client.pelias_autocomplete(search_text, country='PH', layers=['address', 'venue'])
            return Response(results)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
