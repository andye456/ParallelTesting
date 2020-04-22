#!/bin/bash

# This is the test runner script that does the following:
# 1) removes old containers and images
# 2) creates the images
# 3) creates and runs the microservices in the containers, waits until they are complete
# 4) results are written back to the output directory of each test
# 5) rebot collates the results in one place.

#Define the number of test cases
tests=3

for (( i=0; i<tests; i++ ))
do
  docker stop robot${i}
  docker rm robot${i}
  docker image rm tc${i}_robot${i}
  docker stop sut${i}
  docker rm sut${i}
  docker image rm tc${i}_sut${i}
done


echo "The following Images Still running:"
docker images
echo "The following Containers still running:"
docker ps -a

echo "ctl-c  within 5 seconds to abort"
sleep 5

for (( i=0; i<tests; i++ ))
do
  # Create results directories
  echo "***** Starting container ${i} using PORT=808${i}"
  # The port definition is needed here as in order for Compose to change the env variable it must exist
  (PORT=808${i} docker-compose -f test-cases/TC${i}/docker-compose.yml up -d) &
  # Get the pid of each background test
  pids[${i}]=$!
done

# waits for all the tests to finish
for pid in ${pids[*]}
do
  wait $pid
done

sleep 6

./tear-down.sh
