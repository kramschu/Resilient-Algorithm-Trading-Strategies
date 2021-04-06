import json
import requests
import os
import shutil
from django.apps import apps
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from backend.apps.quant_connect.models import Backtest
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class FileManager:
    permission_classes = (IsAuthenticated,)

    def edit_filename(self, request):
        user = list(User.objects.filter(email=request.user).values_list('id', flat=True))[0]        
        params = request.data
        filename = params['filename']
        new_name = params['new_name']
        backtest = Backtest.objects.filter(new_filepath=filename, userid=user)[0]
        backtest.new_filepath = new_name
        backtest.save()
        return JsonResponse({'result': 'success'})

    def delete_file(self, request):
        user = list(User.objects.filter(email=request.user).values_list('id', flat=True))[0]        
        params = request.data
        new_filename = params['filename']
        backtest = Backtest.objects.filter(new_filepath=new_filename, userid=user)[0]
        backtest.delete()
        filename = backtest.orig_filename
        file_dir = f'{settings.BASE_DIR}/backend/apps/quant_connect/results/{filename}'
        for file in os.listdir(file_dir):
            file_path = os.path.join(file_dir, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        shutil.rmtree(f'{settings.BASE_DIR}/backend/apps/quant_connect/results/{filename}', ignore_errors=True)
        file_dir_2 = f'{settings.REACT_APP_DIR}/build/static/{filename}'
        for file in os.listdir(file_dir_2):
            file_path_2 = os.path.join(file_dir_2, file)
            try:
                if os.path.isfile(file_path_2) or os.path.islink(file_path_2):
                    os.unlink(file_path_2)
                elif os.path.isdir(file_path_2):
                    shutil.rmtree(file_path_2)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path_2, e))
        shutil.rmtree(f'{settings.REACT_APP_DIR}/build/static/{filename}', ignore_errors=True)

        return JsonResponse({'result': 'success'})
