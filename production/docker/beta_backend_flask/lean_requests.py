#*********************************************************************************************
# Author: Tommy Armstrong
# Date: 1/31/2021
# Class: CS 467 - Capstone
# Group: Resilient Algorithmic Trading Strategies
# Members: Tommy Armstrong, Kimberly Kramschuster, Kepe Bonner, Jillian Crawley
# 
# File: lean_requests.py
# Purpose: a simple script to run client requests to the API that initiates back tests via the
#          QuantConnect Lean Engine
#
# References:
#  Requests:
#    https://www.w3schools.com/python/module_requests.asp
#  
#**********************************************************************************************

import requests
import json

#check to make sure requests is functional:
response = requests.get('https://httpbin.org/ip')
print('Your IP is {0}'.format(response.json()['origin']))
#end check

BASE_URL_SERVICES='http://0.0.0.0'
def root():
    check_response=requests.get(BASE_URL_SERVICES+':6004/')
    return check_response.text

def algorithm():
    params = dict({
              "algorithm": "BasicTemplateDailyAlgorithm",
              "cash": "5000005"
              })
    headers = {"Content-type": "application/json"}
    check_response=requests.post(BASE_URL_SERVICES+':6004/algorithm',
                                 data=json.dumps(params, indent=4),
                                 headers=headers)
    return check_response.text

def check():
    return algorithm()


print(check())

