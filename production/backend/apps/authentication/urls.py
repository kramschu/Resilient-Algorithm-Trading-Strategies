from django.conf.urls import url
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    url(r'signup', views.UserRegistrationView.as_view(), name='user-registration'),
    url(r'login', views.UserLoginView.as_view(), name='user-login'),
    ]
