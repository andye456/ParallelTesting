# Parallel Testing Docker-compose and Robot Framework

## Introduction
This is an investigation into running Robot Framwwork tests in parallel to speed up test execution.

### System Under Test
A test web endpoint that returns JSON or numbers.
If {"data":110011} is POSTed, then it will return {"returned":110011}
If "data=101110" is POSTed to simulate form data, then 101110 is returned.
If "value=110011" is posted then this is an unexpected variable name and -1 is returned.

### Robot Framework
This framework is chosen for testing using the simple http library

### Docker
The system under test and the Robot tests will run in different containers.

### docker-compose 
Docker compose will be used to run the containers as micro services from the same script.

### Parallel testing
A wrapper bash script is used to implement 3 separate test cases defined above:

* 3 SUT containers will be created from the same test image which is the python web server.

* 3 separate images wil be created for the Robot test cases and a container created for each.

### Results
The results will be written back to a shared location and merged using rebot.

## HOW TO
To run the tests call ./test-runner.sh
This will remove all the old images and containers.
Create the containers
Run the Robot tests against the SUT.
