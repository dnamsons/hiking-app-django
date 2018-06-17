from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from datetime import date
from .models import UserFollowing, UserProfile
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def profile(request, user_id):
    requested_user = get_object_or_404(User, id=user_id) # Checks if requested user exists

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

    args = {'requested_user': requested_user, 'name': name, 'age': age}
    return render(request, 'user/profile.html', args)

def edit_profile(request):
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to edit your profile!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request, 'alert_page.html', args)
    return render(request, 'user/edit_profile.html')

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('firstname')
        surname = request.POST.get('lastname')
        desc = request.POST.get('description')
        country = request.POST.get('country')
        city = request.POST.get('city')
        User.first_name = name
        User.last_name = surname
        # if desc != User.userprofile.description:
        #     User.userprofile.description = desc
        # if country != UserProfile.country:
        #     UserProfile.country = country
        # if city != UserProfile.city:
        #     UserProfile.city = city

        return render(request, 'user/edit/update_profile.html')
    

def follow(request):
    form = followform(request.GET.get(followbtn))
    user.userprofile.following_amount += 1
    requested_user.userprofile.follower_amount += 1
    follow_instance = UserFollowing.objects.create(user=User, followed_user=requested_user)

def unfollow(request):
    if(request.GET.get('unfollowbtn')):
        user.userprofile.following_amount -= 1
        requested_user.userprofile.follower_amount -= 1

