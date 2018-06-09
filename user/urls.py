from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
]