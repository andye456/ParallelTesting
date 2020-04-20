# Example of testing end points with POST body wuery string and JSON
*** Settings ***
Library  HttpLibrary.HTTP

*** Test Cases ***
TC0
    # The webserver conext is sut:8080 as the services name is sut and this is what
    # is used for the DNS name.
    [Documentation]    First test case using query string POST values
    Create HTTP Context  sut:8080
    set request body  data=10011
    POST  /index.html
    ${resp}=  get response status
    response status code should equal  200
    ${body}=  get response body
    response body should contain  data=10011
TC1
    [Documentation]  2nd test using JSON
    Create HTTP Context  sut:8080
    set request body  {"data": 110002}
    POST  /index.html
    ${body}=  get response body
    response body should contain  {"returned": 110002}
TC2
    [Documentation]  Error case sould return -1
    Create HTTP Context  sut:8080
    set request body  value=10011
    POST  /index.html
    ${resp}=  get response status
    response status code should equal  200
    ${body}=  get response body
    response body should contain  data=-1
