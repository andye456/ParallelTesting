#!/bin/bash
# Test suite to run the end-point test in parallel using a varying number of Robot test cases per test.

. ./test-suite-utils.sh

# Runs a number of tests in a varying number of containers depending on the desired number of tests
# per container.
tests_per_container=5
total_tests=50
for i in `seq $tests_per_container $tests_per_container $total_tests`
do
  j=$(($i/$tests_per_container))
  echo "******** Running test $i ********"
  create $i $j
done
mv test_times.csv perf_test_times-${tests_per_container}-$j.csv