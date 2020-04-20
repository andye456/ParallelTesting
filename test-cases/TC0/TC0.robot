*** Settings ***
Library  HttpLibrary.HTTP

*** Test Cases ***
TC0
    # The webserver conext is sut:8080 as the services name is sut and this is what
    # is used for the DNS name.
    [Documentation]    First test case using query string POST values
    Create HTTP Context  sut0:8080
    set request body  data=10011
    POST  /index.html
    ${resp}=  get response status
    response status code should equal  200
    ${body}=  get response body
    response body should contain  data=10011