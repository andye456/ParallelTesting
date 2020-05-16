# Runs a number of tests in a varying number of containers depending on the desired number of tests
# per container.

. ./test-suite-utils.sh

tests_per_container=1
total_tests=10
timeout=120
cores=3
for i in `seq $tests_per_container $tests_per_container $total_tests`
do
  j=$(($i/$tests_per_container))
  echo "******** Running test $i ********"
  create_load $i $j $timeout $cores
done
mv test_times.csv results_${today}/load_test_times-${tests_per_container}-${j}-${timeout}-${cores}.csv
