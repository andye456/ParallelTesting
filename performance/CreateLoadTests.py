# Creates test cases
import os

# Creates the following test scenarios
import re
import sys

"""
Number of tests Parallel Tests
50              1
50              2
50              5
50              10
50              25
50              50
"""


class CreateLoadTests:

# This is the setting section for each robot script
    TC_header = """
*** Settings ***
Library  HttpLibrary.HTTP

*** Test Cases ***
    """

# This is the test case to the robot script and is changed for each test case
    TCn = """
TC{num}
    [Documentation]  Test using JSON POST data
    Create HTTP Context  sut{TC}:{port}
    set request body  {"runtime": {runtime}, "cores":{cores}}
    POST  /index.html
    ${body}=  get response body
    response body should contain  {"returned": {runtime}}
    """


    def __init__(self):
        # self.WORKDIR = "performance"
        # if not os.path.exists(self.WORKDIR):
        #     os.mkdir(self.WORKDIR)
        # os.chdir(self.WORKDIR)
        # Create the test case directory and change to it
        if not os.path.exists("test-cases"):
            os.mkdir("test-cases")
        os.chdir("test-cases")
        print("init dir"+os.getcwd())

    def create_tests(self, number, concurrent, timeout, cores):
        print("create tests start dir = " + os.getcwd())
        test_num=0
        for p in range(0, concurrent):
            port = 8080 + p
            current_test="TC" + str(p)
            # create and move into the current test case.
            if not os.path.exists(current_test):
                os.mkdir(current_test)
            os.chdir(current_test)
            print("creating test in " + os.getcwd())
            with open(current_test + ".robot", "w") as f:
                print("created file TC" + str(p) + ".robot")
                # Write settings
                for line in self.TC_header.splitlines():
                    f.write(line+"\n")
                # write Test Case
                for t in range(0, number):
                    for line in self.TCn.splitlines():
                        new_line=line.replace("{num}", str(test_num)).replace("{port}", str(port)).replace("{TC}", str(p)).replace("{runtime}",str(timeout)).replace("{cores}",str(cores))+"\n"
                        f.write(new_line)
                    test_num+=1
                self.createDockerfile(p)
                self.createCompose(p, port)
            # move out of the current test case.
            os.chdir("..")
            # Change the bash script
            self.edit_bash(concurrent)

    # generates the docker file from the template
    def createDockerfile(self,num):
        print("createDockerfile "+os.getcwd())
        dft = open("../../../auto_gen/DockerfileTemplate", "rt")
        # create a new Dockerfile for this test
        df = open("Dockerfile", "wt")
        for line in dft:
            df.write(line.replace("{num}", str(num)))
        dft.close()
        df.close()

    # generates the dcoker-compose.yml file from the template
    def createCompose(self, num, port):
        print("createCompose: "+os.getcwd())
        dct = open("../../../auto_gen/docker-compose-template.yml", "rt")
        # Create a new docker-compose.yml for this test
        dc = open("docker-compose.yml", "wt")
        for line in dct:
            dc.write(line.replace("{num}", str(num)).replace("{port}", str(port)))
        dct.close()
        dc.close()

    # changes the number of test run in the bash script to match the number of test cases TC*
    def edit_bash(self, num):
        print("edit_bash = "+os.getcwd())
        with open("../test-runner.sh", "r") as f:
            lines = f.readlines()
        with open("../test-runner.sh", "w") as f:
            for line in lines:
                f.write(re.sub("tests=.*", "tests="+str(num), line))




loadtests = CreateLoadTests();
# This creates n tests in m test suites (n*m total tests)
tests_per_suite=sys.argv[1]
test_suites=sys.argv[2]
timeout=sys.argv[3]
cores=sys.argv[4]
print("Creating %s test_suites with %s tests each...using %s cores for %s seconds" % (test_suites, tests_per_suite, cores, timeout))
loadtests.create_tests(int(tests_per_suite), int(test_suites), int(timeout), int(cores))
# loadtests.create_tests(5, 10)

