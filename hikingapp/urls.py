"""hikingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from authentication import views as authentication_views
from user import views as user_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'^signup/$', authentication_views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'authentication/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^user/', include('user.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^map/', include('map.urls')),

    url(r'^ajax/validate_username/$', authentication_views.validate_username, name='validate_username'),
    url(r'^ajax/get_followers/$', user_views.get_followers, name='get_followers'),
    url(r'^ajax/get_followings/$', user_views.get_followings, name='get_followings'),
    url(r'^admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

