from rest_framework import serializers
from .models import UserProfile, Listing, SwapRequest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
            "photo",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        # Validate photo if provided
        photo = attrs.get("photo")
        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2MB
                raise serializers.ValidationError({"photo": "Maximum file size is 2MB"})

            allowed_types = ["image/jpeg", "image/png", "image/webp"]
            if photo.content_type not in allowed_types:
                raise serializers.ValidationError(
                    {"photo": "Only JPEG, PNG, and WebP images are allowed"}
                )

        return attrs

    def create(self, validated_data):
        photo = validated_data.pop("photo", None)
        validated_data.pop("password2")
        password = validated_data.pop("password")

        # Create user without password first
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        # Set password properly
        user.set_password(password)
        user.save()

        # Create profile with photo if provided
        profile_data = {}
        if photo:
            profile_data["photo"] = photo

        # Create profile with defaults for bio and location
        profile = UserProfile.objects.create(
            user=user,
            bio="",  # Default empty bio
            location="",  # Default empty location
            **profile_data
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "bio", "location", "photo"]
        read_only_fields = ["id"]

    def validate_photo(self, value):
        if value:
            # Check file size (2MB)
            if value.size > 2 * 1024 * 1024:
                raise ValidationError("Maximum file size is 2MB")

            # Check file type
            allowed_types = ["image/jpeg", "image/png", "image/webp"]
            if value.content_type not in allowed_types:
                raise ValidationError("Only JPEG, PNG, and WebP images are allowed")
        return value


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"


class SwapRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapRequest
        fields = "__all__"
