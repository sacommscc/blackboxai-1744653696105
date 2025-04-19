from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')

urlpatterns = [
    path('api/', include(router.urls)),
]
