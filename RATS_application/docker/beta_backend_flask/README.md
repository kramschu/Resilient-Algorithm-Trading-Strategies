Make sure that you run the docker file at the same location where the Lean folder exists. The docker build command should be executed from there so that the relative filepaths resolve correctly, otherwise you will get errors building the image.

Build the image with the command:
	docker build -t rats-qclean .

Build the container with the command:
	docker run -dt -p 6004:6004 rats-qclean

Find the container name (or id) with:
	docker container ls
or
	docker ps -a

Bash into the container (access the container terminal) with the command:
	docker exec -it [container name] /bin/bash

Once in the terminal (should automatically be in /Lean/Launcher/bin/Debug ) start the Flask server:
	python app.py

Now on the client side, run: python lean_requests.py 

This should initiate a backtest on the backend with informational output and the json object TotalPerformance should be returned to the client.

NOTE: the Requests python module must be installed on the client side to send requests
	pip install requests

