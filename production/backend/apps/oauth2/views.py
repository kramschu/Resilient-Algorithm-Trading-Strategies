
from django.shortcuts import render

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
import random
import requests
import string


from .components.constants import *


def get_state():
    state=random.choices(string.ascii_letters + string.digits, k=16)
    return ''.join(state)

def get_oauth2_url(request):
    base_url='https://accounts.google.com/o/oauth2/v2/auth'
    response_type='code'
    # Change address to heroku:
    #redirect_uri = 'http://localhost:8000/oauth2/access'
    redirect_uri='https://rats-osu2021.herokuapp.com/oauth2/access'
    scopes='email profile openid'
    state_val = get_state()
    request.session['oauth2_state'] = state_val
    print(state_val)
    request.session.modified = True
    print(request.session.items())
    url = (base_url+'?'+'response_type='+response_type+'&client_id='+client_id+
           '&redirect_uri='+redirect_uri+'&scope='+scopes+'&state='+state_val)
    return JsonResponse({"url": url})

# Create your views here.
def index(request):
    oauth2_url = get_oauth2_url(request)
    return render(request, 'oauth2/index.html', {'url': oauth2_url})


def oauth2(request):
    if request.method == 'GET':
        print(request.session.items())
        query_state = str(request.GET.get('state'))
        saved_state = request.session.get('oauth2_state')
        if query_state != saved_state:
            raise Http404(f'Error: State Value Mismatch\nSaved: {saved_state}\tQuery:{query_state}')
        post_body = {
            'code': request.GET.get('code'),
            'client_id': client_id,
            'client_secret': client_secret,
            # Change address to heroku:
            #'redirect_uri': 'http://localhost:8000/oauth2/access',
            'redirect_uri': 'https://rats-osu2021.herokuapp.com/oauth2/access',
            'grant_type': 'authorization_code'
        }
        res = requests.post(url='https://www.googleapis.com/oauth2/v4/token', json=post_body)
        access_token = res.json()['access_token']

        get_url = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses'
        get_headers = {'Authorization': f'Bearer {access_token}'}
        people_res = requests.get(url=get_url, headers=get_headers)

        name = people_res.json()['names'][0]
        email = people_res.json()['emailAddresses'][0]

        request.session['username'] = email['value']
        request.session['firstname'] = name['givenName']
        request.session['lastname'] = name['familyName']

        signup_data = {
            'email': email['value'],
            'firstname': name['givenName'],
            'lastname': name['familyName'],
            'password': name['givenName']
        }
        
        signup_res = requests.post('https://rats-osu2021.herokuapp.com/api/authentication/signup', json=signup_data)
        print(signup_res)

        #Change address to Heroku:
        #return redirect('http://localhost:3000/oauth2login')
        return redirect('https://rats-osu2021.herokuapp.com/oauth2login')
