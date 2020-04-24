# Creates test cases
import os

# Creates the following test scenarios
import re

"""
Number of tests Parallel Tests
50              1
50              2
50              5
50              10
50              25
50              50
"""


class CreatePerformanceTests:

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
    set request body  {"data": 110002}
    POST  /index.html
    ${body}=  get response body
    response body should contain  {"returned": 110002}
    """


    def __init__(self):
        self.WORKDIR = "performance"
        if not os.path.exists(self.WORKDIR):
            os.mkdir(self.WORKDIR)
        os.chdir(self.WORKDIR)
        # Create the test case directory and change to it
        if not os.path.exists("test-cases"):
            os.mkdir("test-cases")
        os.chdir("test-cases")

    def create_tests(self, number, concurrent):
        test_num=0
        for p in range(0, concurrent):
            port = 8080 + p
            current_test="TC" + str(p)
            # create and move into the current test case.
            if not os.path.exists(current_test):
                os.mkdir(current_test)
            os.chdir(current_test)

            with open(current_test + ".robot", "w") as f:
                print("created file TC" + str(p) + ".robot")
                # Write settings
                for line in self.TC_header.splitlines():
                    f.write(line+"\n")
                # write Test Case
                for t in range(0, number):
                    for line in self.TCn.splitlines():
                        print(line)
                        new_line=line.replace("{num}", str(test_num)).replace("{port}", str(port).replace("{TC}", str(p)))+"\n"
                        print(new_line)
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
        dft = open("../../../auto_gen/DockerfileTemplate", "rt")
        # create a new Dockerfile for this test
        df = open("Dockerfile", "wt")
        for line in dft:
            df.write(line.replace("{num}", str(num)))
        dft.close()
        df.close()

    # generates the dcoker-compose.yml file from the template
    def createCompose(self, num, port):
        dct = open("../../../auto_gen/docker-compose-template.yml", "rt")
        # Create a new docker-compose.yml for this test
        dc = open("docker-compose.yml", "wt")
        for line in dct:
            dc.write(line.replace("{num}", str(num)).replace("{port}", str(port)))
        dct.close()
        dc.close()

    # changes the number of test run in the bash script to match the number of test cases TC*
    def edit_bash(self, num):
        with open("../test-runner.sh", "r") as f:
            lines = f.readlines()
        with open("../test-runner.sh", "w") as f:
            for line in lines:
                f.write(re.sub("tests=.*", "tests="+str(num), line))




perftests = CreatePerformanceTests();
# This creates n tests per m test suites (n*m total tests)
perftests.create_tests(5, 10)

# for test in range(0, 50):
#     # establish a port for this test
#     port = 8080 + test
#
#     if not os.path.exists("TC" + str(test)):
#         os.mkdir("TC" + str(test))
#     os.chdir("TC" + str(test))
#
#     # open the template for the docker file and docker-compose.yml file
#     dft = open("../../DockerfileTemplate", "rt")
#     dct = open("../../docker-compose-template.yml", "rt")
#     # create a new Dockerfile for this test
#     df = open("Dockerfile", "wt")
#     for line in dft:
#         df.write(line.replace("{num}", str(test)).replace("{port}", str(port)))
#
#     dft.close()
#     df.close()
#     # Create a new docker-compose.yml for this test
#     dc = open("docker-compose.yml", "wt")
#     for line in dct:
#         dc.write(line.replace("{num}", str(test)).replace("{port}", str(port)))
#     dct.close()
#     dc.close()
#
#     with open("TC" + str(test) + ".robot", "w") as f:
#         f.write("""
# *** Settings ***
# Library  HttpLibrary.HTTP
#
# *** Test Cases ***
# TC%s
#     # The webserver conext is sut:8080 as the services name is sut and this is what
#     # is used for the DNS name.
#     [Documentation]    Test Case %s using query string POST values
#     Create HTTP Context  sut%s:%s
#     set request body  data=10011
#     POST  /index.html
#     ${resp}=  get response status
#     response status code should equal  200
#     ${body}=  get response body
#     response body should contain  data=10011
#     """ % (test, test, test, port))
#
#     os.chdir("..")
