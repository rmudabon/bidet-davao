from django.urls import path

from geolocation.views import GeoAutoCompleteView

urlpatterns = [
    path('autocomplete/', GeoAutoCompleteView.as_view(), name='autocomplete'),
]