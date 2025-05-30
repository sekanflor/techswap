from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile, Listing, SwapRequest
from .serializers import (
    UserProfileSerializer, 
    ListingSerializer, 
    SwapRequestSerializer,
    UserRegistrationSerializer
)
from .decorators import rate_limit

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @rate_limit(requests=10, window=60)  # 10 requests per minute
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(requests=10, window=60)  # 10 requests per minute
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class SwapRequestViewSet(viewsets.ModelViewSet):
    queryset = SwapRequest.objects.all()
    serializer_class = SwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(requests=10, window=60)  # 10 requests per minute
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
