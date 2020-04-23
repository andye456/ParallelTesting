# Creates test cases
import os

WORKDIR = "auto_gen"
os.chdir(WORKDIR)

# Create the test case directory
if not os.path.exists("test-cases"):
    os.mkdir("test-cases")
os.chdir("test-cases")

for test in range(0, 100):
    # establish a port for this test
    port = 8080+test

    if not os.path.exists("TC"+str(test)):
        os.mkdir("TC"+str(test))
    os.chdir("TC"+str(test))

    # open the template for the docker file and docker-compose.yml file
    dft = open("../../DockerfileTemplate", "rt")
    dct = open("../../docker-compose-template.yml", "rt")
    # create a new Dockerfile for this test
    df = open("Dockerfile", "wt")
    for line in dft:
        df.write(line.replace("{num}", str(test)).replace("{port}", str(port)))

    dft.close()
    df.close()
    # Create a new docker-compose.yml for this test
    dc = open("docker-compose.yml", "wt")
    for line in dct:
        dc.write(line.replace("{num}",str(test)).replace("{port}",str(port)))
    dct.close()
    dc.close()

    with open("TC"+str(test)+".robot", "w") as f:
        f.write("""
*** Settings ***
Library  HttpLibrary.HTTP

*** Test Cases ***
TC%s
    # The webserver conext is sut:8080 as the services name is sut and this is what
    # is used for the DNS name.
    [Documentation]    Test Case %s using query string POST values
    Create HTTP Context  sut%s:%s
    set request body  data=10011
    POST  /index.html
    ${resp}=  get response status
    response status code should equal  200
    ${body}=  get response body
    response body should contain  data=10011
    """ % (test, test, test, port ))

    os.chdir("..")


