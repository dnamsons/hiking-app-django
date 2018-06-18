from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from posts.models import UserPost


# Create your views here. 

def search(request):
    if request.user.is_anonymous:
        alert_message = 'You must be logged in to use search!'
        alert_type = 'danger'
        args = {'alert_message': alert_message, 'alert_type': alert_type}
        return render(request, 'alert_page.html', args)
    query = request.GET.get('q', None)

    if query != None and query != '':
        users = User.objects.filter(username__contains = query)
        args = {'query': query, 'users': users}
    
    else:
        query = None
        args = {'query': query}

    return render(request, 'search/search.html', args)