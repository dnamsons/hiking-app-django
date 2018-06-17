from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
    url(r'^edit/update/$', views.update_profile, name='update_profile'),
    url(r'^(?P<user_id>\d+)/follow/$', views.follow, name='follow'),
    url(r'^(?P<user_id>\d+)/unfollow/$', views.unfollow, name='unfollow'),
]