*** Settings ***
Library  HttpLibrary.HTTP

*** Test Cases ***
TC2
    [Documentation]  Error case sould return -1
    Create HTTP Context  sut2:8082
    set request body  value=10011
    POST  /index.html
    ${resp}=  get response status
    response status code should equal  200
    ${body}=  get response body
    response body should contain  data=-1