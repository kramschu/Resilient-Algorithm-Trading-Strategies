"""RATS_application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls import include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('api/quant_connect/', include('apps.quant_connect.urls')),
    path('oauth2/', include('apps.oauth2.urls')),
    path('cred/', include('apps.cred.urls')),
    # Namespace URLs
    re_path('^quant_connect',
            TemplateView.as_view(template_name='quant_connect.html'),
            name='quant_connect'),

    # Anything else redirect to home
    # 02-14-2021 - Note from Tommy: the below re_path line caused a url of type /endpoint and 
    # type /endpoint/ to be redirected to different views. It caused exact matching of
    # the path strings in the above urlpatterns rather than matching to both: 'endpoint' and 'endpoint/'

    #re_path('^(?:.*)/?$', RedirectView.as_view(url='/'))
]
