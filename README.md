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

#### Scaling
The performance of the parallel testing is in no doubt when 3 tests are run in parallel compared to in series.
This test will explore how many tests can be run in parallel using docker containers on a single machine.
The initial aim is 100 Robot tests against 100 web servers. 


### Results
The results will be written back to a shared location and merged using rebot.

## HOW TO
To run the tests call ./test-runner.sh from {home} location, this calls set-up.sh and tear-down.sh, these can be commented out if
you don't want to re-create the images or create the results.

To auto generate the tests for soak tests then call {home}/CreateTestCases.py. This will create auto_gen/test-cases/TC{0-100}

To run the tests call test-runner.sh from auto_gen. By default this will clear out the old docker containers adn images and recreate them.

## Troubleshooting
##### If you can only run 31 tests at a time it's because the docker network range is restricting this. To solve add the following:

/etc/docker/daemon.json

    {
        "default-address-pools":
            [
                    {"base":"10.10.0.0/16", "size":24}
            ]
    }
    
Restart the docker daemon

    sodo systemctl restart docker

##### Temporary failure in name resolution [Errno -3] with Docker. Docker cannot contact pypi.python.org.
    vi /etc/default/docker

Uncomment the DOCKER_OPTS dns lookup bit.

If you still get problems then add the following to /etc/docker/daemon.json at the top level of the json doc if already there.
   
    {
        "dns": ["10.1.2.3", "8.8.8.8"]
    }
    
Restart the docker daemon

    sodo systemctl restart docker