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
from django.views.generic import View
from django.views.generic import TemplateView, RedirectView
from . import views

urlpatterns = [
    path('', views.FrontendAppView.as_view()),
    path('cred/', include('backend.apps.cred.urls')),
    path('api/quant_connect/', include('backend.apps.quant_connect.urls')),
    path('api/authentication/', include('backend.apps.authentication.urls')),
    path('oauth2/', include('backend.apps.oauth2.urls')),
    # Namespace URLs
    re_path('^quant_connect',
            TemplateView.as_view(template_name='quant_connect.html'),
            name='quant_connect'),

    # Anything else redirect to home
    re_path(r'^', views.FrontendAppView.as_view()),
    path('^$', views.FrontendAppView.as_view()),
]

