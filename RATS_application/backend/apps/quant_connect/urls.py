from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Tests/', views.get_tests, name='get_tests'),
    url(r'algorithm_manager/set_algorithm',
        views.set_algorithm,
        name="algorithm-manager-set-algorithm"),
    url(r'algorithm_manager/get_past_runs',
        views.get_past_runs,
        name="algorithm-manager-get-past-runs"),
    path('getdb', views.getdb, name='getdb')
]
