import subprocess
import os
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from flask import request
from django.conf import settings
from datetime import date, datetime
from ..models import *
import requests
import json


class AlgorithmManager:

    def _run_algorithm(self, params):
        check_response = requests.post(settings.BASE_URL_SERVICES + ':6004/algorithm',
                                        json=params
                                        )

        return check_response.text

    def set_algorithm(self, request):
        params = request.data
        print(params)
        algorithm_results = json.loads(self._run_algorithm(params))
        filepath = settings.RATS_BACKEND_DIR + "/quant_connect/results/" + request.data['algorithm'] + '_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.json'
        with open(filepath, 'w') as f:
            json.dump(algorithm_results, f, indent=4)
        # backtest = Backtest(algname=params["algorithm"],
        #                     cash=params["cash"],
        #                     buytol=params["buytol"] ,
        #                     selltol=params["selltol"],
        #                     startdate=datetime(params["startdate"][0], params["startdate"][1], params["startdate"][2]).strftime("%Y%m%d"),
        #                     enddate=datetime(params["enddate"][0], params["enddate"][1], params["enddate"][2]).strftime("%Y%m%d"),
        #                     userid=User.objects.get(pk=1),
        #                     filepath=filepath
        #                     )
        # backtest.save()
        return JsonResponse(algorithm_results)

    def get_past_runs(self, request):
        files_dir = settings.RATS_BACKEND_DIR + "/quant_connect/results/"
        past_runs = os.listdir(files_dir)
        return JsonResponse({'past_runs': past_runs})
