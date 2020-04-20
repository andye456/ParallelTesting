*** Settings ***
Library  HttpLibrary.HTTP

*** Test Cases ***
TC1
    [Documentation]  2nd test using JSON
    Create HTTP Context  sut1:8081
    set request body  {"data": 110002}
    POST  /index.html
    ${body}=  get response body
    response body should contain  {"returned": 110002}