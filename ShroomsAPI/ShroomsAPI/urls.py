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
from django.conf.urls import include, url
from django.contrib import admin

from adherents.views import (SubscribeView, SubscriptionTypeViewSet,
                             SubscriptionViewSet, AdherentViewSet)
from profiles.views import (OrganisationViewSet, ProfileGroupViewSet,
                            ProfileViewSet, OrganisationGroupViewSet)
from rest_framework_extensions.routers import ExtendedDefaultRouter
from users.views import GroupViewSet, UserViewSet

admin.autodiscover()


drf_router = ExtendedDefaultRouter()
# users app
drf_router.register(r'users', UserViewSet)
drf_router.register(r'groups', GroupViewSet)
# profiles app
drf_router.register(r'profiles', ProfileViewSet)
drf_router.register(r'profiles-groups', ProfileGroupViewSet)
drf_router.register(r'organisations', OrganisationViewSet)
drf_router.register(r'organisations-groups', OrganisationGroupViewSet)
# adherents app
drf_router.register(r'adherents', AdherentViewSet)
drf_router.register(r'subscriptions', SubscriptionViewSet)
drf_router.register(r'subscription-types', SubscriptionTypeViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^activity/', include('actstream.urls')),
    url(r'^subscribe/', SubscribeView.as_view(), name='subscribe'),
    url(r'^', include(drf_router.urls)),
]

auth_patterns = [
    # Djoser + JWT
    url(r'^auth/', include('users.urls')),
    # OAuth
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns += auth_patterns


def show_urls(urllist, depth=0):
    """
    Print URL patterns
    """
    for entry in urllist:
        print("\t" * depth, entry.regex.pattern)
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)


# Show urls at start-up during development
if settings.DEBUG:
    show_urls(urlpatterns)
