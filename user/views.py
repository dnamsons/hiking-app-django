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


def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    

def follow(request):
    form = followform(request.GET.get(followbtn))
    user.userprofile.following_amount += 1
    requested_user.userprofile.follower_amount += 1
    follow_instance = UserFollowing.objects.create(user=User, followed_user=requested_user)

def unfollow(request):
    if(request.GET.get('unfollowbtn')):
        user.userprofile.following_amount -= 1
        requested_user.userprofile.follower_amount -= 1

