import subprocess
import os
from rest_framework import status
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from flask import request
from django.conf import settings
from datetime import date, datetime
from ..models import *
from django.contrib.auth import authenticate, login
# Custom serializer class built atop django abstract generic classes:
from backend.apps.authentication.serializers import UserRegistrationSerializer
from backend.apps.authentication.serializers import UserLoginSerializer
import requests
import json


class Authentication:
    def login(self, request):
        # the extended serializer that we coded earlier:
        serializer_class = UserLoginSerializer
        # Passes request data to crete a form object serializer. here, 'serializer':
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Sending success response along with JWT token if valid:
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "User logged in  successfully",
            "username": serializer.data["email"],
            "token": serializer.data["token"],
        }
        status_code = status.HTTP_200_OK

        return JsonResponse(response, status=status_code)

    def register(self, request):
        # serializer helps to retrieve data and parse it into json and vice versa
        # It also checks for exceptions: Validates whether data from POST request can be injected into the DB
        # It checks which fields are required in the models.py and sends an exception message accordingly

        # Telling which serializer to use:
        serializer_class = UserRegistrationSerializer

        # Function for incoming POST requests: To inject the new user data into our DB
        # OR return exception message in JSON format if some data is inappropriate or missing
        user_data = {
            'email': request.data['email'],
            'profile': {
                'first_name': request.data['firstname'],
                'last_name': request.data['lastname'],
            },
            'password': request.data['password']
        }
        serializer = serializer_class(data=user_data)
        # validates if it doesnt violate model/schema rules
        # Uses serializers.py for validation
        serializer.is_valid(raise_exception=True)
        # Adding the user into our DB
        serializer.save()
        # Stub response to let frontend know that the registration was successful
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "User registered  successfully",
        }
        status_code = status.HTTP_200_OK
        return JsonResponse(response, status=status_code)