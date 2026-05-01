from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import HealthCheckView, UploadView
from .views import LocationViewSet

router = routers.DefaultRouter()
router.register(r"locations", LocationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("users/", include("users.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('health/', HealthCheckView.as_view(), name='health')
]