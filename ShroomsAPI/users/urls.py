from django.conf.urls import include, url
from django.contrib.auth import get_user_model

import rest_framework_jwt.views as drf_jwt
from djoser import views as djoser_views

User = get_user_model()

urlpatterns = (
    url(r'^me/$', djoser_views.UserView.as_view(), name='user'),
    url(r'^register/$', djoser_views.RegistrationView.as_view(), name='register'),
    url(r'^activate/$', djoser_views.ActivationView.as_view(), name='activate'),
    url(r'^{0}/$'.format(User.USERNAME_FIELD),
        djoser_views.SetUsernameView.as_view(), name='set_username'),
    url(r'^password/$', djoser_views.SetPasswordView.as_view(),
        name='set_password'),
    url(r'^password/reset/$', djoser_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password/reset/confirm/$',
        djoser_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^login', drf_jwt.obtain_jwt_token, name='login'),
    url(r'^refresh_token', drf_jwt.refresh_jwt_token, name='refresh_token'),
    url(r'^verify_token', drf_jwt.verify_jwt_token, name='verify_token'),
    url(r'^logout/$', djoser_views.LogoutView.as_view(), name='logout'),
    url(r'^$', djoser_views.RootView.as_view(urls_extra_mapping={
        'login': 'login',
        'logout': 'logout',
        'refresh': 'refresh_token',
        'verify': 'verify_token'}), name='root'),
)
