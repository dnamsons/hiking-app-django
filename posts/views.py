from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserComment, UserLike, UserPost
from user.forms import ImageUploadForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your views here.

def post_belong_to_user(author_id, user_id):
    if(author_id == user_id):
        return True
    else:
        return False

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

def edit_post(request, post_id):
    post = UserPost.objects.get(post_id = post_id)
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to edit your profile!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request,'alert_page.html', args)
    if not post_belong_to_user(request.user.id, post.post_author.id):
        alert_message = 'You can not edit post, that you do not own!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request,'alert_page.html', args)
    args = {
        'post': post
    }
    return render(request, 'posts/editpost.html', args)

def update_post(request, post_id):
    post = UserPost.objects.get(post_id = post_id)
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to edit your profile!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request,'alert_page.html', args)
    if not post_belong_to_user(request.user.id, post.post_author.id):
        alert_message = 'You can not edit post, that you do not own!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request,'alert_page.html', args)

    if request.method == 'POST':
        new_text = request.POST.get('post_content')
        if new_text == post.post:
            alert_message = 'No changes have been made!'
            alert_type = 'warning'
            args = {'alert_message': alert_message, 'alert_type': alert_type}
            return render(request,'alert_page.html', args)
        elif new_text != '':
            post.post = new_text
            post.save()
        else:
            alert_message = 'Post can not be empty!'
            alert_type = 'danger'
            args = {'alert_message': alert_message, 'alert_type': alert_type}
            return render(request,'alert_page.html', args)
        return render(request, 'user/edit/update_profile.html')
    else:
        return render(request, '/')
        

def delete_post(request, post_id):
    url = reverse('home')
    UserPost.objects.get(post_id = post_id).delete()
    return HttpResponseRedirect(url)
    


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
    user_like = UserLike.objects.filter(post_id=post_id, like_author=user_id).first()

    if(request_type == 'minus'):
        if not user_like:
            UserLike.objects.create(like_author = user, post_id = post, like_type = '-')
            post.like_amount = post.like_amount - 1
            post.save()
            response = 'okminuscreated_' + str(post.like_amount)
        elif user_like and user_like.like_type == '+':
            post.like_amount = post.like_amount - 1
            post.save()
            user_like.delete()
            response = 'okplusnowdoesntexist_' + str(post.like_amount)
        elif user_like and user_like.like_type == '-':
            response = 'badisalreadyminus_' + str(post.like_amount)

    else:
        if not user_like:
            UserLike.objects.create(like_author = user, post_id = post, like_type = '+')
            post.like_amount = post.like_amount + 1
            post.save()
            response = 'okpluscreated_' + str(post.like_amount)
        elif user_like and user_like.like_type == '-':
            post.like_amount = post.like_amount + 1
            post.save()
            user_like.delete()
            response = 'okmminusnowdoesntexist_' + str(post.like_amount)
        elif user_like and user_like.like_type == '+':
            response = 'badisalreadyplus_' + str(post.like_amount)
    return JsonResponse({'response': response, 'like_count': post.like_amount})