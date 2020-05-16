# Parallel Testing Docker-compose and Robot Framework

## Introduction
This is an investigation into running Robot Framework tests in parallel to speed up test execution.

### System Under Test
A test web endpoint that returns JSON or numbers.
If {"data":110011} is POSTed, then it will return {"returned":110011}
If "data=101110" is POSTed to simulate form data, then 101110 is returned.
If "value=110011" is posted then this is an unexpected variable name and -1 is returned.

#### Process loading
If {"runtime":120, "cores":1} is POSTed then the SUT will run an additional Python script on the container hosting the web server that loads the number of 
cores indicated for 'run' seconds. The loading script (do_load.py) adds a floating point number in a loop, when the process
finishes the number it has counted up to is written to a file. This can then be used to measure performance.

### Robot Framework
This framework is chosen for testing using the simple http library

### Docker
The system under test and the Robot tests will run in different containers.

### docker-compose 
Docker compose will be used to run the containers as micro services from the same script.

### Parallel testing
A wrapper bash script is used to implement 3 separate test cases defined above:

* Many SUT containers will be created from the same test image which is the python web server.

* Many separate images wil be created for the Robot test cases and a container created for each.

#### Scaling
The performance of the parallel testing is in no doubt when a few tests are run in parallel compared to in series.
This test will explore how many tests can be run in parallel using docker containers on a single machine.
The initial aim is 100 Robot tests against 100 web servers. 

### Results
The results will be written back to a shared location and merged using Rebot.

## HOW TO
### Basic Usage
Work from the root of this project :
The SUT is in ~/sut, this is a basic web server that will return by default a web page after 5 seconds
If the request for this page contains {"runtime":120, "cores":1}, say, then the web page will load 1 core of the processors to 100% and return after 120 seconds.
The robot scripts for basic manual tests are in ~/test-cases/TC*
The performnace test suites are created automatically by performance/CreatePerformanceTests.py
These directories are robot test scripts that test the web server response.
### Automation
#### Create many parallel containers, each running one test. 

To auto generate the tests for stress tests then call {home}/CreateTestCases.py. This will create auto_gen/test-cases/TC{0-100}

To run the tests call ./test-runner.sh from {home} location, this calls set-up.sh and tear-down.sh, these can be commented out if
you don't want to re-create the images or create the results.

To run the tests call test-runner.sh from auto_gen. By default this will clear out the old docker containers adn images and recreate them.

### Performance
#### Create parallel tests each containing a varied number of tests
There may be a point where it is better to have less containers running more tests as the overhead of running the tests becomes significant 
and the docker network for the particular host gets too slow.

* Delete the old test directories under performance/test-cases/TC* (you need to do this as root as the shared output directory is written to as root)
* In the root directory edit the script CreatePerformanceTests.py and adjust the number of tests and the number of containers - this is the number of tests per container
* In the directory {root}/performance edit test-runner.sh and make sure the number of test = number of containers.
* Check the containers and images currently in existance. docker ps -a, docker images. Remove if necessary docker image rm {name}, docker rm $(docker ps -a -q)

cd performance
./test-suite-run-AxB.sh

The times for each iteration of the parallel suite, e.g. 1 test per container 1 - 50 containers in parallel, will produce 50 timings that are written to a file test_time.csv.
At the end of the test this file is moved to perf_test_times-${tests_per_container}-${containers}.csv

Running graph.py will read all the perf*.csv files form the performance directory and plot on a graph.

#### Load Tests
These tests are designed to test the performance of parallel testing when the processor is under load by the SUT. 
The sharing of resources will affect the performance of the tests and the SUT if running in parallel.
These tests load-test-run-1x10-n.sh will run 1 test per container, with 1 - 10 parallel tests running loading on n cores.
There are 6 tests in this suite, which run the tests with an increasing processor load.
Also from this test suite is a performance metric for the SUT, this is created by the SUT writing it's progress during the tests
to a text file.

#### MatplotLib graphs
graph.py will read the perf-test-times*.csv files from the performance (current) directory ad plot a graph, this is the time it takes to run
an increasing number of 5 second tests in parallel.
load_graph.py will read the load-test-times_1_10_t_c.csv (where t is run time and c is cores under load.)
sut_perf_graph.py will read n-SUT-perf.csv (where n is the number of cores loaded) and produce a graph of the SUT performance.
(NOTE1: only the first 55 results for each SUT-perf file as taking the information for all cores overwhelms the graph, this assumes that the performance is the same)
(NOTE2: It is actually the rebot helper file, do_load.py in ~/sut, that produced the performance data and writes the SUT-perf.csv files. 
The performance data is written to a file in the directory /SUT/output in the container caled n-<datetime.txt, this is then mounted to performance/test-cases/TCn/output in the docker-compose.yml file
which is auto generate from the template file ~/auto_gen/docker-compose-template.yml, when the test tears down the performance data file is written to the results_<date> directory)

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