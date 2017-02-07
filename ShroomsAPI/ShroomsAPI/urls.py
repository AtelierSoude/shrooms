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
                             SubscriptionViewSet, UserSubscriptionViewset)

from profiles.views import (AdminOrganisationViewSet, AdminProfileGroupViewSet,
                            AdminUserProfileViewSet, ProfileViewSet)
from rest_framework_extensions.routers import ExtendedDefaultRouter
from users.views import GroupViewSet, UserViewSet




admin.autodiscover()


drf_router = ExtendedDefaultRouter()
# users app
drf_router.register(r'users', UserViewSet)
drf_router.register(r'groups', GroupViewSet)
# profiles app
drf_router.register(r'profiles', AdminUserProfileViewSet)
drf_router.register(r'profile-groups', AdminProfileGroupViewSet)
drf_router.register(r'organisations', AdminOrganisationViewSet)
# adherents app
drf_router.register(r'subscriptions', SubscriptionViewSet)
drf_router.register(r'subscription-types', SubscriptionTypeViewSet)


user_router = ExtendedDefaultRouter()
user_router.register(r'profile', ProfileViewSet, base_name='profile').register(
    r'subscriptions', UserSubscriptionViewset, base_name='user-subscriptions', parents_query_lookups=['adherent'])

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^activity/', include('actstream.urls')),
    #url(r'^admin-api/', include(drf_router.urls)),
    #url(r'^me/', include(user_router.urls)),
    url(r'^api/subscribe/', SubscribeView.as_view(), name='subscribe'),
    url(r'^api/', include(user_router.urls, namespace='profile')),
    #url(r'^api/', include(profile_router.urls)),
]

auth_patterns = [
    # Djoser + JWT
    url(r'^auth/', include('users.urls')),
    #OAuth
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
