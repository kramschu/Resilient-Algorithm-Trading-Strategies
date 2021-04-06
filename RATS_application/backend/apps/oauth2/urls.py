from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='oauth2_index'),
    path('access', views.oauth2, name='oauth2_access'),
    path('url', views.get_oauth2_url, name='oauth2_url')
    
]