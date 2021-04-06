from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .components.tests import Test
from django.views.decorators.csrf import csrf_exempt
from .components.algorithm_manager import AlgorithmManager
from .models import *
from django.core import serializers as core_serializers
from django.http import JsonResponse

def index(request):
    return (request, "templates/quant_connect.html")


def get_tests(request):
    return Tests().get_tests(request, 'quant_connect.html')

def getdb(request):
    users = User.objects.all()
    backtests = Backtest.objects.all()
    print(users, backtests)
    json_data = core_serializers.serialize('json', backtests)
    return JsonResponse(json_data, safe = False)

@api_view(['POST'])
def set_algorithm(request):
    return AlgorithmManager().set_algorithm(request)


@api_view(['GET'])
def get_past_runs(request):
    return AlgorithmManager().get_past_runs(request)