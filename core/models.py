from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
import os

def validate_file_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:  # 2MB in bytes
        raise ValidationError("Maximum file size is 2MB")

def crop_to_square(image):
    width, height = image.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    return image.crop((left, top, right, bottom))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    location = models.CharField(max_length=100)
    photo = models.ImageField(
        upload_to='profile_photos/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            # Open the image
            img = Image.open(self.photo.path)
            # Crop to square
            img = crop_to_square(img)
            # Save the cropped image
            img.save(self.photo.path)

    def clean(self):
        if self.photo:
            validate_file_size(self.photo)

    def __str__(self):
        return self.user.username

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SwapRequest(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.requester.username} for {self.listing.title}"
