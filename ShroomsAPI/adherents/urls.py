from django.conf.urls import url, include
from adherents.views import SubscribeView

urlpatterns = [
    url(r'^subscribe/', SubscribeView.as_view())
]