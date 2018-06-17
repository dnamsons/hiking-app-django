from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from datetime import date
from .models import UserFollowing, UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from django.core.urlresolvers import reverse

# Create your views here.

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def profile(request, user_id):
    requested_user = get_object_or_404(User, id=user_id) # Checks if requested user exists
    current_user = request.user
    followed = False
    if current_user != requested_user:
        if UserFollowing.objects.filter(user = current_user, followed_user = requested_user).exists():
            followed = True
            


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

    args = {'requested_user': requested_user, 'name': name, 'age': age, 'followed': followed}
    return render(request, 'user/profile.html', args)

def edit_profile(request):
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to edit your profile!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request, 'alert_page.html', args)
    return render(request, 'user/edit_profile.html')

# FIXME: redirect to profile/id, shouldn't stay on profile/id/follow or unfollow, as you can't unfollow/follow straight after

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('firstname')
        surname = request.POST.get('lastname')
        desc = request.POST.get('description')
        country = request.POST.get('country')
        city = request.POST.get('city')
        current_user = request.user
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
    
@csrf_exempt
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

    

    
@csrf_exempt
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

