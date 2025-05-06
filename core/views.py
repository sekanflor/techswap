from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import UserProfile, Listing, SwapRequest
from .serializers import UserProfileSerializer, ListingSerializer, SwapRequestSerializer
from .decorators import rate_limit

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(requests=100, window=60)  # 100 requests per minute
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(requests=100, window=60)  # 100 requests per minute
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class SwapRequestViewSet(viewsets.ModelViewSet):
    queryset = SwapRequest.objects.all()
    serializer_class = SwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(requests=100, window=60)  # 100 requests per minute
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
