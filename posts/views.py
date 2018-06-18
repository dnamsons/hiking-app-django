from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserComment, UserLike, UserPost
from user.forms import ImageUploadForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your views here.

def create_post(request):
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to make a post!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request, 'alert_page.html', args)
    return render(request, 'posts/newpost.html')

def make_post(request):
    url = reverse('home')
    if request.method == 'POST':
        current_user = request.user
        post_contents = request.POST.get('post_content')
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            UserPost.objects.create(post_author = current_user, post = post_contents, image = form.cleaned_data['image'])
        else:
            UserPost.objects.create(post_author = current_user, post = post_contents)
    return HttpResponseRedirect(url)

def edit_post(request):
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to edit your profile!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request, 'alert_page.html', args)
    return render(request, 'posts/editpost.html')

# def make_edit(request):

# def delete_post(request):
    


def render_own_posts(request):
    current_user = request.user
    post_query = UserPost.objects.filter(post_author = current_user)
    if not post_query:
        return None
    return post_query

def render_other_posts(request, requested_user):
    post_query = UserPost.objects.filter(post_author = requested_user)
    if not post_query:
        return None
    return post_query

def modify_like(request):
    request_type = request.GET.get('request_type', None)
    user_id = request.GET.get('user_id', None)
    post_id = request.GET.get('post_id', None)

    response = 'bad'

    if(request_type == None or user_id == None or post_id == None):
         return JsonResponse({'response': response})

    user = User.objects.get(id=user_id)
    post = UserPost.objects.filter(post_id=post_id).first()
    like_count = post.like_amount
    user_like = UserLike.objects.filter(post_id=post_id, like_author=user_id)

    if(request_type == 'minus'):
        if user_like:
            post.like_amount = post.like_amount - 1
            post.save()
            user_like.delete()
            response = 'okminus' + str(post.like_amount)
        else:
            response = 'minus_bad_doesnt_exist'
    else:
        if not user_like:
            post.like_amount = post.like_amount + 1
            post.save()
            UserLike.objects.create(post_id=post, like_author=user)
            response = 'okplus' + str(post.like_amount)
        else:
            response = 'plus_bad_exists'
    return JsonResponse({'response': response, 'like_count': post.like_amount})