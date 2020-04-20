FROM python:2.7

COPY Server.py /SUT/Server.py
COPY index.html /SUT/index.html

ARG PORT
ENV p PORT
WORKDIR /SUT

# The server is run using the port set in the environment variable PORT in the individual containers.
CMD ["python", "Server.py"]

