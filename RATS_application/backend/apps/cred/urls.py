from django.urls import path
from django.conf.urls import url
from .views import GetUser, UserLogout

urlpatterns = [
    path('user', GetUser.as_view()),
    path('logout', UserLogout.as_view()),
    
]