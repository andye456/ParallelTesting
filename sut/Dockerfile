FROM python:2.7

COPY Server.py /SUT/Server.py
COPY do_load.py /SUT/do_load.py
COPY index.html /SUT/index.html

ARG PORT

RUN mkdir -p /SUT/output
WORKDIR /SUT

# The server is run using the port set in the environment variable PORT in the individual containers.
CMD ["python", "Server.py"]

