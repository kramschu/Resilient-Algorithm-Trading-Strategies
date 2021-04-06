from django.shortcuts import render, HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
# Create your views here.


class GetUser(APIView):
    # Allows users without JWT auth to request for registration:
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        
        email = self.request.session.get('username')
        firstname = self.request.session.get('firstname')
        lastname = self.request.session.get('lastname')

        data = {'logged_in': False}
        status_code = status.HTTP_204_NO_CONTENT
        if email != None:
            data = {
                'username': email,
                'logged_in': True,
                'email': email,
                'firstname': firstname,
                'lastname': lastname
            }
            status_code = status.HTTP_200_OK
        return JsonResponse(data, status=status_code)


class UserLogout(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, format=None):
        self.request.session.flush()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)