
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ListingViewSet, SwapRequestViewSet

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'swap-requests', SwapRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
