# admin.py placeholder

from django.contrib import admin
from .models import UserProfile, Listing, SwapRequest

admin.site.register(UserProfile)
admin.site.register(Listing)
admin.site.register(SwapRequest)
