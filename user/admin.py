from django.contrib import admin

from .models import UserFollowing, UserProfile

# Register your models here.

admin.site.register(UserFollowing)
admin.site.register(UserProfile)