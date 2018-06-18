from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserComment, UserLike, UserPost
from user.forms import ImageUploadForm
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
