#!/bin/bash
# This bash script is called after the tests have run
# 1) Shows the docker logs for each test
# 2) Runs rebot with the modifier scripts to produce a correct elapsed time for the test suite
# 3) Stops all the containers and removes the images - this is necessary for resource reasons.
[[ $# -ne 1 ]] && echo arg1 = number of tests && exit 1
#tests=$1
#echo "test logs"
#for (( i=0; i<tests; i++ ))
#do
#  docker logs robot${i}
#done
#rebot --prerebotmodifier ../RebotGetElapsedTests.py --prerebotmodifier ../RebotGetElapsedSuite.py -d output -N "Test Suite" test-cases/TC*/output/*.xml
#
for (( i=14; i<18; i++ ))
do
  (
  echo "Stopping and removing containers and images $i"
  docker stop robot${i}
  docker rm robot${i}
  docker image rm tc${i}_robot${i}
  docker stop sut${i}
  docker rm sut${i}
  docker image rm tc${i}_sut${i}
  )&
done
