from django.db import models
from django.contrib.auth.models import User
import os


def get_image_path(instance, filename):
    return os.path.join('posts', str(instance.id), filename) #/media/user/<userid>/joke.png

# Create your models here.
class UserPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    post = models.CharField(max_length=500, default='', blank=True)
    like_amount = models.IntegerField(default=0)
    comment_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class UserComment(models.Model):
    post_id = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='%(class)s_author')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')
    comment = models.CharField(max_length=200, default='', blank=True)

class UserLike(models.Model):
    post_id = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='%(class)s_author')
    like_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')
