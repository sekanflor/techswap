from rest_framework import serializers
from .models import UserProfile, Listing, SwapRequest
from django.core.exceptions import ValidationError

class UserProfileSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'location', 'photo']
        read_only_fields = ['id']

    def validate_photo(self, value):
        if value:
            # Check file size (2MB)
            if value.size > 2 * 1024 * 1024:
                raise ValidationError("Maximum file size is 2MB")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
            if value.content_type not in allowed_types:
                raise ValidationError("Only JPEG, PNG, and WebP images are allowed")
        return value

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

class SwapRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapRequest
        fields = '__all__'
