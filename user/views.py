from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from datetime import date


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
    #current_user = request.user
    #truefalse = user_id == current_user.id # Checks whether logged in user is accesing his page

    args = {'user': requested_user, 'name': name, 'age': age}
    return render(request, 'user/profile.html', args)