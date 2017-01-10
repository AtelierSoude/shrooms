"""ShroomsAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from users.views import *

admin.autodiscover()


def print_url_pattern_names(patterns):
    """Print a list of urlpattern and their names"""
    for pat in patterns:
        if pat.__class__.__name__ == 'RegexURLResolver':
            print_url_pattern_names(pat.url_patterns)
        elif pat.__class__.__name__ == 'RegexURLPattern':
            if pat.name is not None:
                print('[API-URL] {} \t\t\t-> {}'.format(pat.name, pat.regex.pattern))

drf_router = DefaultRouter()
drf_router.register(r'users', UserViewSet)
drf_router.register(r'permissions', PermissionViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^activity/', include('actstream.urls')),
    url(r'^api/', include(drf_router.urls)),
    url(r'^api/', include('users.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    print_url_pattern_names(urlpatterns)
