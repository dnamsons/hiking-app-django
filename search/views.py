from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here. 

def search(request):
    query = request.GET.get('q', None)

    if query != None and query != '':
        users = User.objects.filter(username__contains = query)
        # Velak pec si pasa principa pievienosim komentarus, routes utt.
        args = {'query': query, 'users': users}
    
    else:
        query = None
        args = {'query': query}

    return render(request, 'search/search.html', args)