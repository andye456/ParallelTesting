#!/bin/bash
# This bash script is called after the tests have run
# 1) Shows the docker logs for each test
# 2) Runs rebot with the modifier scripts to produce a correct elapsed time for the test suite
# 3) Stops all the containers and removes the images - this is necessary for resource reasons.
# The script RebotGetElapsedSuite.py also creates a csv file that is used to plot the graphs
[[ $# -ne 1 ]] && echo arg1 = number of tests && exit 1
today=`date +%Y-%m-%d`
tests=$1
echo "test logs"
for (( i=0; i<tests; i++ ))
do
  docker logs robot${i}
done
# This concatenates the results of all the parallel tests that go to make up this test-suit and puts the result log.html in ~/performance/test-cases/output.
rebot --prerebotmodifier ../RebotGetElapsedTests.py --prerebotmodifier ../RebotGetElapsedSuite.py -d results_${today} -N "Test Suite" test-cases/TC*/output/*.xml
# Gets the SUT performance results from the x-mounted directory
for (( i=0; i<tests+1; i++ )); do
  echo "***** Copying tests from test-cases/TC${i}/output/*.txt to results_${today}/"
  cp test-cases/TC${i}/output/*.txt results_${today}
done

# Removes all of the containers and images in parallel
for (( i=0; i<tests; i++ ))
do
  (
  echo "Stopping and removing containers and images $i"
  docker stop robot${i}
  docker rm robot${i}
  docker image rm tc${i}_robot${i}
  docker stop sut${i}
  docker rm sut${i}
  docker image rm tc${i}_sut${i}
  ) &
done
