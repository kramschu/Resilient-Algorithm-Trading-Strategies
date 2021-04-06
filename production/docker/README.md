Build the image with the command: docker build -t rats-qclean .

Build the container and start flask with the command:  docker run -dt -p 6004:6004 rats-qclean bash -c "(python app.py)"
