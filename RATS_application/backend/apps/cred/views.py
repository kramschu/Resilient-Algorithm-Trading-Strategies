from django.shortcuts import render, HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

class GetUser(APIView):
    def get(self, request, format=None):
        user = self.request.session.get('username')
        print(user)
        data = {'logged_in': False}
        status_code = status.HTTP_404_NOT_FOUND
        if user != None:
            data = {
                'username': self.request.session.get('username'),
                'logged_in': True
            }
            status_code = status.HTTP_200_OK
        return JsonResponse(data, status=status_code)

class UserLogout(APIView):
    def get(self, request, format=None):
        self.request.session.flush()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

