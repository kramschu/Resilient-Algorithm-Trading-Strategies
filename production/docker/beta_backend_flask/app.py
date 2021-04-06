#*********************************************************************************************
# Author: Tommy Armstrong
# Date: 1/31/2021
# Class: CS 467 - Capstone
# Group: Resilient Algorithmic Trading Strategies
# Members: Tommy Armstrong, Kimberly Kramschuster, Kepe Bonner, Jillian Crawley
# 
# File: app.py
# Purpose:  Backend API running in the docker container hosting the Quant Connect Lean Engine
#           that receives requests from the user interface and returns results from backtests
# Run Command: python app.py
#
# Module References:
#  Sed:
#    http://unixmysimpleview.blogspot.com/2010/03/sed-more-intro.html
#    https://superuser.com/questions/112834/how-to-match-whitespace-in-sed
#    https://stackoverflow.com/questions/8822097/how-to-replace-a-whole-line-with-sed
#    https://www.gnu.org/software/sed/manual/html_node/Command_002dLine-Options.html
#    https://www.cyberciti.biz/faq/unix-linux-sed-match-replace-the-entire-line-command/
# 
#  JSON:
#    https://www.programiz.com/python-programming/json
#
#  Flask:
#    https://flask.palletsprojects.com/en/1.1.x/
#    https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
#    
#**********************************************************************************************

from flask import Flask, make_response, render_template, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def root():                  
    return 'Hello World'

@app.route('/algorithm', methods=['POST'])
def run_algorithm():
    params=request.get_json()
    print(params)

    # Begin modifying files to match specification of requested algorithm backtest
    print('Running sed commands')
    algo=params.get('algorithm')
    # Set the Algorithm Type Name value in the config.json file
    algo_type_command=f'sed -i \'s|^[ \t]*"algorithm-type-name".*|  "algorithm-type-name": "{algo}",|\' /Lean/Launcher/bin/Debug/config.json'
    os.system(algo_type_command)
    # Set the Algorithm Location value in the config.json file
    algo_loc_command=f'sed -i \'s|^[ \t]*"algorithm-location".*|  "algorithm-location": "/Lean/Algorithm.Python/{algo}.py",|\' /Lean/Launcher/bin/Debug/config.json'
    os.system(algo_loc_command)
    print('Finished sed commands')

    # Set the value for the starting cash value in the Algorithm Python file
    print('Setting cash values in Python files')
    cash=params.get('cash')
    cash_command=f'sed -i \'s|^VAR_CASH.*|VAR_CASH={cash}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(cash_command)
    print('Finished setting cash values in python files')

    # Initiate the backtest run
    print('Launching lean backtest')
    lean_command='echo -e "\n" | mono QuantConnect.Lean.Launcher.exe >/dev/null 2>&1'
    os.system(lean_command)
    print('Finished lean backtest')

    # Retrieve the JSON results of the backtest and load them as a dictionary
    print('Loading JSON backtest results file')
    results_fp=f'/Lean/Results/{algo}.json'
    with open(results_fp) as f:
        results = json.load(f)
    total_performance=results.get('TotalPerformance')

    # Return the backtest results to the client
    print(total_performance)
    headers = {'Content-Type': 'application/json'}
    return make_response(total_performance, 200, headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6004, debug=True)