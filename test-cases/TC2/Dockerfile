FROM python:2.7

# make sure the repo is there
RUN ping -c 1 pypi.python.org
RUN python -m pip install robotframework
RUN python -m pip install robotframework-httplibrary

RUN mkdir -p /SUT/test
RUN mkdir -p /SUT/output

COPY TC2.robot /SUT/test/

WORKDIR /SUT/test

CMD robot -d /SUT/output TC2.robot