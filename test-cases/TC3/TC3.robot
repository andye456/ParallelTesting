*** Settings ***
Library  HttpLibrary.HTTP

*** Test Cases ***
TC3
    [Documentation]  Returns after 10 seconds of heavy load to simulate a SUT
    Create HTTP Context  sut3:8083

    set request body  {"sleep": 10, "cores": 6}
    POST  /index.html
    ${resp}=  get response status
    response status code should equal  200
    ${body}=  get response body
    response body should contain  {"returned": 10}
