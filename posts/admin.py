from django.contrib import admin
from .models import UserPost, UserComment, UserLike

# Register your models here.

admin.site.register(UserPost)
admin.site.register(UserComment)
admin.site.register(UserLike)