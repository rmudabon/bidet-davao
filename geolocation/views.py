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
            features = results.get('features', [])
            first_five_suggestions = features[:5] if features else []
            parsed_suggestions = []
            for suggestion in first_five_suggestions:
                properties = suggestion.get('properties', {})
                geometry = suggestion.get('geometry', {})
                coordinates = geometry.get('coordinates', [None, None])
                parsed_suggestions.append({
                    'label': properties.get('label'),
                    'street': properties.get('street'),
                    'name': properties.get('name'),
                    'longitude': coordinates[0], # ORS returns [long, lat]
                    'latitude': coordinates[1]
                })

            return Response(parsed_suggestions)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GeoReverseGeoCodingView(APIView):
    client = openrouteservice.Client(key=settings.ORS_API_KEY)

    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        if not latitude or not longitude:
            return Response({"error": "Missing 'latitude' or 'longitude' query parameter."}, status=status.HTTP_400_BAD_REQUEST)
        point = [float(longitude), float(latitude)]  # ORS expects [lon, lat]
        
        try:
            results = self.client.pelias_reverse(point, country='PH', layers=['address', 'venue'], size=1)
            features = results.get('features', [])
            if features:
                properties = features[0].get('properties', {})
                parsed_features = {
                    'label': properties.get('label'),
                    'street': properties.get('street'),
                }

                return Response(parsed_features)
            return Response(results)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
