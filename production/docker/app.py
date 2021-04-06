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
#  Subprocess:
#    https://stackoverflow.com/questions/15119188/python-subprocess-write-new-line-to-stdin-until-process-ends
#    https://stackoverflow.com/questions/2837214/python-popen-command-wait-until-the-command-is-finished
#    https://stackoverflow.com/questions/16768290/understanding-popen-communicate
#    https://gist.github.com/ajdavis/6222554
#    
# 
# History:
# 21Feb2021 TommyArmstrong - Added an endpoint for generating the report html
#**********************************************************************************************

from datetime import datetime
from flask import Flask, abort, make_response, render_template, request, jsonify, send_from_directory
import json
import os
import subprocess
import time
from werkzeug.utils import secure_filename
from zipfile import ZipFile


app = Flask(__name__)

PORT = os.getenv('PORT')

report_images = ['monthly-returns.png', 'cumulative-return.png', 'annual-returns.png', 'returns-per-trade.png',
                 'asset-allocation-backtest.png', 'drawdowns.png']

ALLOWED_EXTENSIONS = ['py']

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.route('/')
def root():
    return '<h1>Hello World<h1>'


@app.route('/algorithm', methods=['POST'])
def run_algorithm():
    params = request.get_json()
    print('***********')
    print('***********')
    print(params)

    # Begin modifying files to match specification of requested algorithm backtest
    print('Running sed commands')
    algo = params.get('algorithm')
    # Set the Algorithm Type Name value in the config.json file
    algo_type_command = f'sed -i \'s|^[ \t]*"algorithm-type-name".*|  "algorithm-type-name": "{algo}",|\' /Lean/Launcher/bin/Debug/config.json'
    os.system(algo_type_command)
    # Set the Algorithm Location value in the config.json file
    algo_loc_command = f'sed -i \'s|^[ \t]*"algorithm-location".*|  "algorithm-location": "/Lean/Algorithm.Python/{algo}.py",|\' /Lean/Launcher/bin/Debug/config.json'
    os.system(algo_loc_command)
    print('Finished sed commands')

    # Set the value for the starting cash value in the Algorithm Python file
    print('Setting cash values in Python files')
    cash = int(params.get('cash'))
    cash_command = f'sed -i \'s|^VAR_CASH.*|VAR_CASH={cash}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(cash_command)
    print('Finished setting cash values in python files')

    # Set the values for the starting date
    print('Setting start date in the python file')
    startlist = params.get('startdate')
    startyear = int(startlist[2])
    startmonth = int(startlist[0])
    startday = int(startlist[1])
    start_year = f'sed -i \'s|^START_YEAR.*|START_YEAR={startyear}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(start_year)
    start_month = f'sed -i \'s|^START_MONTH.*|START_MONTH={startmonth}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(start_month)
    start_day = f'sed -i \'s|^START_DAY.*|START_DAY={startday}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(start_day)
    print('Finished setting up start date in python files')

    # Set the values for the end date
    print('Setting end date in the python file')
    endlist = params.get('enddate')
    endyear = int(endlist[2])
    endmonth = int(endlist[0])
    endday = int(endlist[1])
    end_year = f'sed -i \'s|^END_YEAR.*|END_YEAR={endyear}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(end_year)
    end_month = f'sed -i \'s|^END_MONTH.*|END_MONTH={endmonth}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(end_month)
    end_day = f'sed -i \'s|^END_DAY.*|END_DAY={endday}|\' /Lean/Algorithm.Python/{algo}.py'
    os.system(end_day)
    print('Finished setting up ending dates in python files')

    # Initiate the backtest run
    print('Launching lean backtest')
    lean_command = 'echo -e "\n" | mono QuantConnect.Lean.Launcher.exe >/dev/null 2>&1'
    os.system(lean_command)
    print('Finished lean backtest')

    # Retrieve the JSON results of the backtest and load them as a dictionary
    print('Loading JSON backtest results file')
    results_fp = f'/Lean/Results/{algo}.json'
    with open(results_fp) as f:
        results = json.load(f)

    # Return the backtest results to the client
    return jsonify(results)

@app.route('/report/<backtest_id>', methods=['GET'])
def send_report(backtest_id):
    algo = backtest_id.split('_')[0]
    timestamp = backtest_id.split('_')[1]
    if algo == None:
        return abort(404, description='algorithm is missing in request parameters')

    backtest_results = f'/Lean/Results/{algo}.json'
    if os.path.isfile(backtest_results) != True:
        return abort(404, description='algorithm backtest results don\'t exist')
        
    report_results_folder=f'/Lean/Results/Report/{backtest_id}'
    os.system(f'mkdir {report_results_folder}')

    exe_dir = '/Lean/Report/bin/Debug'
    exe_report = f'{exe_dir}/QuantConnect.Report.exe'
    report_name = f'{backtest_id}.html'
    report_path = f'{report_results_folder}/{report_name}'

    strategy_name_command = f'sed -i \'s|^[ \t]*"strategy-name".*|  "strategy-name": "{algo}",|\' /Lean/Report/bin/Debug/config.json'
    os.system(strategy_name_command)

    strategy_desc_command = f'sed -i \'s|^[ \t]*"strategy-description".*|  "strategy-description": "{algo}",|\' /Lean/Report/bin/Debug/config.json'
    os.system(strategy_desc_command)

    backtest_results_command = f'sed -i \'s|^[ \t]*"backtest-data-source-file".*|  "backtest-data-source-file": "{backtest_results}",|\' /Lean/Report/bin/Debug/config.json'
    os.system(backtest_results_command)

    report_dest_command = f'sed -i \'s|^[ \t]*"report-destination".*|  "report-destination": "{report_path}",|\' /Lean/Report/bin/Debug/config.json'
    os.system(report_dest_command)

    results_dest_command = f'sed -i \'s|^[ \t]*"results-destination-folder".*|  "results-destination-folder": "{report_results_folder}",|\' /Lean/Report/bin/Debug/config.json'
    os.system(results_dest_command)

    print("*****************************************************")
    print("                  Creating Report                    ")

    report_process = subprocess.Popen([
        'mono', exe_report], 
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=exe_dir)
    report_process.communicate("\n")
    
    print("                  Report Created                   ")
    print(f'Report Path: {report_path}')
    print("*****************************************************")

    z_filename = f'{backtest_id}_report_content.zip'
    z_filepath = f'{report_results_folder}/{z_filename}'
    z_file = ZipFile(z_filepath, 'w')
    
    print('Writing report images to zip file')
    for image in report_images:
        z_file.write(f'{exe_dir}/{image}', arcname=image)
    # z_file.write(report_path, arcname=report_name)
    # z_file.write(f'{report_results_folder}/{backtest_id}-backtesting-portfolio.json', arcname=f'{backtest_id}-backtesting-portfolio.json')
    z_file.close()
    print('Closed zip file')
    # print(z_file.printdir())
    return send_from_directory(report_results_folder, z_filename, as_attachment=True)


@app.route('/report/delete/<backtest_id>', methods=['DELETE'])
def delete_report(backtest_id):
    report_results_folder = f'/Lean/Results/Report/{backtest_id}'
    if os.path.isdir(report_results_folder) != True:
        return abort(404, description='report results folder doesn\'t exist')
    
    remove_command = f'rm -rf {report_results_folder}'

    print("*****************************************************")
    print("           Deleting Report Directory                 ")

    os.system(remove_command)

    print("            Report Directory Deleted                 ")
    print(f'Report Folder Path: {report_results_folder}')
    print("*****************************************************")

    return (f'Deleted Report: {backtest_id} Successfully', 204)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/algorithm/upload', methods=['POST'])
def upload_algorithm():
    algorithm_folder = '/Lean/Algorithm.Python'
    if 'file' not in request.files:
        return abort(400, description='File not attached to request')
    algo_file = request.files['file']
    if algo_file and allowed_file(algo_file.filename):
        filename = secure_filename(algo_file.filename)
        algo_file.save(os.path.join(algorithm_folder, filename))
        return (f'Uploaded File Successfully: {filename}')
    else:
        abort(400, 'File and/or filename is missing')

@app.route('/algorithm/list', methods=['GET'])
def algorithm_list():
    algorithm_folder = '/Lean/Algorithm.Python/'
    algorithms = [ filename for filename in os.listdir(algorithm_folder) if filename.endswith('.py') ]
    return jsonify(algorithms=algorithms)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=(int(PORT) if PORT else 6004), debug=True)
