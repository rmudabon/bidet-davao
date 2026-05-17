from django.urls import path

from geolocation.views import GeoAutoCompleteView, GeoReverseGeoCodingView

urlpatterns = [
    path('autocomplete/', GeoAutoCompleteView.as_view(), name='autocomplete'),
    path('reverse/', GeoReverseGeoCodingView.as_view(), name='reverse-geocoding'),
]