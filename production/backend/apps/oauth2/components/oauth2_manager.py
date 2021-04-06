from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.template import loader
import random
import requests
import string


from .constants import *


class OAuth2Manager:

    def get_state(self):
        state = random.choices(string.ascii_letters + string.digits, k=16)
        return ''.join(state)

    def get_oauth2_url(self, request):
        base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        response_type = 'code'
        redirect_uri = 'http://localrats.com:8000/oauth2/access'
        scopes = 'email profile openid'
        state_val = self.get_state()
        request.session['state'] = state_val
        url = (base_url+'?'+'response_type='+response_type+'&client_id='+client_id+
            '&redirect_uri='+redirect_uri+'&scope='+scopes+'&state='+state_val)
        return url

    # Create your views here.
    def index(self, request):
        oauth2_url = self.get_oauth2_url(request)
        return render(request, 'oauth2/index.html', {'url': oauth2_url})

    def oauth2(self, request):
        if request.method == 'GET':
            query_state = str(request.GET.get('state'))
            saved_state = request.session['state']
            if query_state != saved_state:
                raise Http404(f'Error: State Value Mismatch\nSaved: {saved_state}\tQuery:{query_state}')
            post_body = {
                'code': request.GET.get('code'),
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': 'http://localrats.com:8000/oauth2/access',
                'grant_type': 'authorization_code'
            }
            res = requests.post(url='https://www.googleapis.com/oauth2/v4/token', json=post_body)
            access_token = res.json()['access_token']

            get_url = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses'
            get_headers = {'Authorization': f'Bearer {access_token}'}
            people_res = requests.get(url=get_url, headers=get_headers)
            print(people_res.json())
            name = people_res.json()['names'][0]
            email = people_res.json()['emailAddresses'][0]
            display_data = {
                'firstname': name['givenName'],
                'lastname': name['familyName'],
                'email': email['value'],
                'state': saved_state
            }
            return render(request, 'oauth2/user_info.html', {'data': display_data})