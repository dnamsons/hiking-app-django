from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from posts import views as post_view


urlpatterns = [
    url(r'^new/$', post_view.create_post, name='newpost'),
    url(r'^new/make_post/$', post_view.make_post, name='makepost'),
    url(r'^edit_post/(?P<post_id>\d+)/$', post_view.edit_post, name='editpost'),
    url(r'^edit_post/(?P<post_id>\d+)/delete/$', post_view.delete_post, name='deletepost'),
    url(r'^edit_post/(?P<post_id>\d+)/update/$', post_view.update_post, name='updatepost')
] 