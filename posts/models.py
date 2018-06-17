from django.db import models

# Create your models here.
class UserPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, default='images/no_image.jpg')
    post = models.CharField(max_length=300, default='', blank=True)
    like_amount = models.IntegerField(default=0)
    comment_amount = models.IntegerField(default=0)

class UserComment(models.Model):
    post_id = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='%(class)s_author')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')
    comment = models.CharField(max_length=200, default='', blank=True)

class UserLike(models.Model):
    post_id = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='%(class)s_author')
    like_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')
