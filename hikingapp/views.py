from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from user.models import UserFollowing, UserProfile
from posts.models import UserPost, UserLike, UserComment

# Create your views here.

def home(request):
    if(User.is_authenticated):

        posts = UserPost.objects.filter(post_author=request.user.id)

        user_following = UserFollowing.objects.filter(user = request.user.id)

        for following in user_following:
            user_post = UserPost.objects.filter(post_author=following.followed_user)
            posts = posts | user_post

        posts = posts.order_by('-created_at')
        post_count = posts.count()

    args = {
        'post_list': posts,
        'post_count': post_count
    }
    return render(request, 'home.html', {'args': args})