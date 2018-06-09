from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('user', str(instance.id), filename) #/media/users/<userid>/joke.png

class UserProfile(models.Model): # Piesaistits originalajam user
    user = models.OneToOneField(User)
    description = models.CharField(max_length=300, default='', blank=True) #blank true lai liktu mieraa
    birthdate= models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    city = models.CharField(max_length=50, default='', blank=True)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True) # izmanto pip install Pillow
    
    def __str__(self): # Svarigi nodefinet, lai nebutu "UserProfile object" bet "lietotajs_profile"
        return self.user.username + '_profile'

def create_profile(sender, **kwargs):
    if kwargs['created']: # If post_save user - created, then save the user profile
        user_profile = UserProfile.objects.create(user=kwargs['instance']) # Asociee userprofile ar izveidoto user


# Post save, lai lietotaja izveidosanas bridi tiktu izveidots ari vina profils.
post_save.connect(create_profile, sender=User)

class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user_that_is_following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user_that_is_beign_followed')
    def __str__(self):
        return self.user.username + '_follows_' + self.followed_user.username