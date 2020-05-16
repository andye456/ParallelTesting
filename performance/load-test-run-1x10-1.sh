# Runs a number of tests in an increasing number of containers each test runs a SUT on 1 CPU core.

. ./test-suite-utils.sh

tests_per_container=1
total_tests=10
timeout=120
cores=1
# seq start_val increment max_val
for i in `seq $tests_per_container $tests_per_container $total_tests`
do
  j=$(($i/$tests_per_container))
  echo "******** Running test $i ********"
  create_load $i $j $timeout $cores
done
mv test_times.csv results_${today}/load_test_times-${tests_per_container}-${j}-${timeout}-${cores}.csv
