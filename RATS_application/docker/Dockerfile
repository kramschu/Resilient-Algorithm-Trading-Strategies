#
#   LEAN Docker Container 20200522
#   Cross platform deployment for multiple brokerages
#

# Use base system
FROM quantconnect/lean:foundation

MAINTAINER QuantConnect <contact@quantconnect.com>

#Update apt repository
RUN apt-get update
#Install net-tools
RUN apt-get install net-tools

#Install Python Tool for Visual Studio Debugger for remote python debugging
RUN pip install ptvsd

#Install PyDev Debugger for Pycharm for remote python debugging
RUN pip install pydevd-pycharm~=201.8538.36

RUN pip install Flask==1.1.2

COPY ./Lean/ /Lean/

RUN nuget restore /Lean/QuantConnect.Lean.sln
RUN msbuild /Lean/QuantConnect.Lean.sln

COPY ./app.py /Lean/Launcher/bin/Debug/
RUN cp /Lean/Launcher/config.json /Lean/Launcher/bin/Debug/
RUN cp /Lean/Report/config_report.json /Lean/Report/bin/Debug/
RUN mkdir /Lean/Results/Report

# Can override with '-w'
WORKDIR /Lean/Launcher/bin/Debug/

# Set default port number to 6004
ENV PORT=6004
EXPOSE ${PORT}

# Start the backend Flask app to interface with the Lean engine
CMD ["python", "/Lean/Launcher/bin/Debug/app.py"]

# Following app line to be included when development is complete
#ENTRYPOINT ["python", "main.py"]