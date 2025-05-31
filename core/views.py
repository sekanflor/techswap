from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile, Listing, SwapRequest
from .serializers import (
    UserProfileSerializer,
    ListingSerializer,
    SwapRequestSerializer,
    UserRegistrationSerializer,
)
from .decorators import rate_limit


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Get user profile and photo URL
        profile = UserProfile.objects.get(user=user)
        photo_url = (
            request.build_absolute_uri(profile.photo.url) if profile.photo else None
        )

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Format user data for response
        user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo": photo_url,
        }

        return Response(
            {
                "user": user_data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


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
