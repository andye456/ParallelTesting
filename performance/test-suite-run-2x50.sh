# Runs a number of tests in a varying number of containers depending on the desired number of tests
# per container.

. ./test-suite-utils.sh

tests_per_container=2
total_tests=50
for i in `seq $tests_per_container $tests_per_container total_tests`
do
  j=$(($i/$tests_per_container))
  echo "******** Running test $i ********"
  create $i $j
done
mv test_times.csv perf_test_times-${tests_per_container}-$j.csv

