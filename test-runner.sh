#!/bin/bash

# This is the test runner script that does the following:
# 1) removes old containers and images
# 2) creates the images
# 3) creates and runs the microservices in the containers, waits until they are complete
# 4) results are written back to the output directory of each test
# 5) rebot collates the results in one place.

#Define the number of test cases
tests=10

./set-up.sh $tests

echo "ctl-c  within 5 seconds to abort"
sleep 5

for (( i=0; i<tests; i++ ))
do
  port=$((8080+$i))
  # Create results directories
  echo "***** Starting container ${i} using port + ${i}"
  # The port definition is needed here as in order for Compose to change the env variable it must exist
  (PORT=$port docker-compose -f test-cases/TC${i}/docker-compose.yml up -d) &
  # Get the pid of each background test
  pids[${i}]=$!
done

# waits for all the tests to finish
for pid in ${pids[*]}
do
  wait $pid
done

# Wait until all the containers have stopped then tear-down
sleep 6
while [[ 1==1 ]]; do
  if [[ `docker ps | grep robot` == "" ]]
  then
    ./tear-down.sh $tests
    exit 0
  fi
  sleep 10
  echo "waiting!"
done
