from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from datetime import date
from .models import UserFollowing, UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from user.forms import ImageUploadForm
from posts.views import render_own_posts, render_other_posts

# Create your views here.

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def profile(request, user_id):
    requested_user = get_object_or_404(User, id=user_id) # Checks if requested user exists
    current_user = request.user
    followed = False
    if current_user != requested_user:
        post_list = render_other_posts(request, requested_user)
        if UserFollowing.objects.filter(user = current_user, followed_user = requested_user).exists():
            followed = True
    else:
        post_list = render_own_posts(request)


    if requested_user.first_name != '':
        if requested_user.last_name != '':
            name = requested_user.first_name + ' ' + requested_user.last_name
        else:
            name = requested_user.first_name
    else:
        name = requested_user.username
    
    if requested_user.userprofile.birthdate != None:
        age = calculate_age(requested_user.userprofile.birthdate)
    else:
        age = None
    
    

    args = {'requested_user': requested_user, 'name': name, 'age': age, 'followed': followed, 'post_list': post_list,}
    return render(request, 'user/profile.html', args)

def edit_profile(request):
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to edit your profile!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request, 'alert_page.html', args)
    return render(request, 'user/edit_profile.html')

def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('firstname')
        surname = request.POST.get('lastname')
        desc = request.POST.get('description')
        country = request.POST.get('country')
        city = request.POST.get('city')
        current_user = request.user
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if current_user.userprofile.profile_image != 'images/no_image.jpg':
                current_user.userprofile.profile_image.delete()
            current_user.userprofile.profile_image = form.cleaned_data['image']
            current_user.userprofile.save()
        if name != current_user.first_name:
            current_user.first_name = name
        if surname != current_user.last_name:
            current_user.last_name = surname 
        current_user.save()
        if desc != current_user.userprofile.description:
            current_user.userprofile.description = desc
        if country != current_user.userprofile.country:
            current_user.userprofile.country = country
        if city != current_user.userprofile.city:
            current_user.userprofile.city = city
        current_user.userprofile.save()
        
        

        return render(request, 'user/edit/update_profile.html')
    
def follow(request, user_id):
    url = reverse('profile', kwargs={'user_id': user_id})
    requested_user = get_object_or_404(User, id=user_id)

    if(UserFollowing.objects.filter(user = request.user.id, followed_user = user_id).exists()):
        return HttpResponseRedirect(url)
    
    else:
        current_user = request.user
        requested_user.userprofile.follower_amount += 1
        requested_user.userprofile.save()
        current_user.userprofile.following_amount += 1
        current_user.userprofile.save()
        follow_instance = UserFollowing.objects.create(user=current_user, followed_user=requested_user)
    return HttpResponseRedirect(url)

    

def unfollow(request, user_id):
    url = reverse('profile', kwargs={'user_id': user_id})
    requested_user = get_object_or_404(User, id=user_id)
    current_user = request.user
    requested_user.userprofile.follower_amount -= 1
    requested_user.userprofile.save()
    current_user.userprofile.following_amount -= 1
    current_user.userprofile.save()
    follow_instance = UserFollowing.objects.filter(user=current_user, followed_user=requested_user).delete()
    return HttpResponseRedirect(url)

def get_followers(request):
    requested_user_id = request.GET.get('requested_user_id', None)
    followers = UserFollowing.objects.filter(followed_user = requested_user_id)
    data = []
    for follower in followers:
        if(follower.user.userprofile.profile_image):
            img_path = follower.user.userprofile.profile_image.url
        else:
            img_path = "/media/images/no_image.jpg"

        lieta = {
            'user_id': follower.user.id,
            'username': follower.user.username,
            'picture': img_path
        }
        data.append(lieta)

    return JsonResponse({'user_id': requested_user_id, 'data': list(data)})

def get_followings(request):
    requested_user_id = request.GET.get('requested_user_id', None)
    followings = UserFollowing.objects.filter(user = requested_user_id)

    data = []
    for following in followings:
        if(following.followed_user.userprofile.profile_image):
            img_path = following.followed_user.userprofile.profile_image.url
        else:
            img_path = "/media/images/no_image.jpg"

        lieta = {
            'user_id': following.followed_user.id,
            'username': following.followed_user.username,
            'picture': img_path
        }
        data.append(lieta)

    return JsonResponse({'user_id': requested_user_id, 'data': list(data)})