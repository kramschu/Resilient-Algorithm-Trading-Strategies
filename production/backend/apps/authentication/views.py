from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .components.authentication import Authentication
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView, RetrieveAPIView


class UserRegistrationView(RetrieveAPIView):
    # Allows users without JWT auth to request for registration:
    permission_classes = (AllowAny,)

    def post(self, request):
        # Allows users without JWT auth to request for registration:
        print(request)
        return Authentication().register(request)


class UserLoginView(RetrieveAPIView):
    # Allows users without JWT auth to request for registration:
    permission_classes = (AllowAny,)

    def post(self, request):
        return Authentication().login(request)
