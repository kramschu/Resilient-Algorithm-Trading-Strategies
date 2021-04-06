import subprocess
import os, shutil
import re, mmap
import json
import requests
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from flask import request
from django.conf import settings
from datetime import date, datetime
from backend.apps.quant_connect.models import Backtest
from rest_framework.permissions import IsAuthenticated
from zipfile import ZipFile

User = get_user_model()


class AlgorithmManager:
    permission_classes = (IsAuthenticated,)

    def _run_algorithm(self, params):
        os.environ['NO_PROXY'] = '0.0.0.0'
        session = requests.Session()
        session.verify = False
        check_response = session.post('http://35.238.162.119:6004/algorithm',
                                        json=params, verify=False
                                        )

        return check_response.text

    def set_algorithm(self, request):
        params = request.data
        algo = params['algorithm']
        user = User.objects.get(email=request.user)
        backtest_id = f'{algo}_{str(datetime.now().strftime("%Y%m%dT%H%M%S"))}'
        backtest_dir = settings.BASE_DIR + "/backend/apps/quant_connect/results/" + backtest_id
        if os.path.isdir(backtest_dir) != True:
            os.system(f'mkdir {backtest_dir}')
        algorithm_results = json.loads(self._run_algorithm(params))
        backtest_file = f'{backtest_dir}/{backtest_id}.json'
        with open(backtest_file, 'w') as f:
            json.dump(algorithm_results, f, indent=4)
        backtest = Backtest(algname=params["algorithm"],
                            cash=params["cash"],
                            orig_filepath=backtest_id,
                            new_filepath=backtest_id,
                            startdate=datetime(int(params["startdate"][2]), int(params["startdate"][0]), int(params["startdate"][1])).strftime("%Y%m%d"),
                            enddate=datetime(int(params["enddate"][2]), int(params["enddate"][0]), int(params["enddate"][1])).strftime("%Y%m%d"),
                            userid=user,
                            )
        backtest.save()

        report_response = requests.get(f'http://35.238.162.119:6004/report/{backtest_id}')
        print('Received Report from Lean Engine Server')
        print(report_response)
        zfile_info = report_response.headers.get('content-disposition')
        print('************')
        print(zfile_info)
        zfile_name = str(re.findall('filename=(.+)', zfile_info)[0])
        print(zfile_name)
        backtest_id = zfile_name.split('_report')[0]
        print(backtest_id)
        backtest_dir = settings.BASE_DIR + '/backend/apps/quant_connect/results/' + backtest_id
        if os.path.isdir(backtest_dir) != True:
            os.system(f'mkdir {backtest_dir}')
        save_to_zfile = f'{backtest_dir}/{zfile_name}'
        print(f'Saving Report to Django Backend')
        zip_file_data = report_response.content

        with open(save_to_zfile, 'wb') as f:
            f.write(zip_file_data)
        print(f'Report Saved to: {save_to_zfile}')

        z_file = ZipFile(save_to_zfile, 'r')
        z_file.extractall(backtest_dir)
        # Delete zipfile now that contents are extracted
        os.system(f'rm -f {save_to_zfile}')
        # Request for the report directory on the Lean Engine server to be deleted
        delete_report_response = requests.delete(f'http://35.238.162.119:6004/report/delete/{backtest_id}')
        
        return JsonResponse({'backtest_id': backtest_id})

    def get_past_runs(self, request):
        user = list(User.objects.filter(email=request.user).values_list('id', flat=True))[0]
        user_runs = list(Backtest.objects.filter(userid=user).values_list('new_filepath', flat=True))
        return JsonResponse({'past_runs': user_runs})

    def get_past_data(self, request):
        new_file = request.data['file_name']
        file_object = Backtest.objects.filter(new_filepath=new_file)[0]
        orig_file = file_object.orig_filepath
        filepath = f'{settings.BASE_DIR}/backend/apps/quant_connect/results/{orig_file}/{orig_file}.json'
        file_string = f'{settings.BASE_DIR}/backend/apps/quant_connect/results/{orig_file}/'
        with open(filepath) as f:
            data = json.load(f)

        statistics = data['Statistics']
        print(statistics)
        total_trades = statistics['Total Trades']
        win_rate = statistics['Win Rate']
        loss_rate = statistics['Loss Rate']
        average_win = statistics['Average Win']
        average_loss = statistics['Average Loss']
        profit = statistics['Net Profit']
        compounding_annual_return = statistics['Compounding Annual Return']
        drawdown = statistics['Drawdown']
        prelim_strat_chart = data['Charts']['Strategy Equity']['Series']['Equity']['Values']
        prelim_benchmark_chart = data['Charts']['Benchmark']['Series']['Benchmark']['Values']     
        strat_chart = {
            'x': [prelim.get('x') for prelim in prelim_strat_chart],
            'y': [prelim.get('y') for prelim in prelim_strat_chart],
            'type': 'scatter',
        }
        benchmark_chart = {
            'x': [prelim.get('x') for prelim in prelim_benchmark_chart],
            'y': [prelim.get('y') for prelim in prelim_benchmark_chart],
            'type': 'scatter',
        }

        img_files = [f'{file_string}drawdowns.png', f'{file_string}annual-returns.png',
            f'{file_string}asset-allocation-backtest.png', f'{file_string}cumulative-return.png',
            f'{file_string}monthly-returns.png', f'{file_string}returns-per-trade.png']
 
        try: 
            os.mkdir(f'{settings.REACT_APP_DIR}/build/static/{orig_file}')
            for image in img_files:
                shutil.copy(image, f'{settings.REACT_APP_DIR}/build/static/{orig_file}/')
        except:
            pass

        return JsonResponse({
            'orig_filepath': orig_file,
            'strat_chart': strat_chart,
            'benchmark_chart': benchmark_chart,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'average_win': average_win,
            'average_loss': average_loss,
            'profit': profit,
            'compounding_annual_return': compounding_annual_return,
            'drawdown': drawdown
        })

    def upload_algorithm(self, request):
        # Send the attached file to the Docker Backend
        upload_response = requests.post(f'http://35.238.162.119:6004/algorithm/upload', files=request.FILES)
        print(upload_response)
        return JsonResponse({'info': 'file uploaded to docker backend'})

    def get_algorithms(self, request):
        list_response = requests.get(f'http://35.238.162.119:6004/algorithm/list')
        algorithms = [algorithm.split('.py')[0] for algorithm in list_response.json()['algorithms']]
        algorithms.sort()
        return JsonResponse({'algorithms': algorithms})


