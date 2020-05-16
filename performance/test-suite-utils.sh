# A function to create the test cases and tidy up afterwards by removing the test-case directories
# Prameters:
# The number of tests to create
# The number of test suites used to run these tests
today=`date +%Y-%m-%d`

function create {
	tests=$1
  suites=$2
	tests_per_suite=$(($tests/$suites))
	echo "`date`: Creating $tests tests in $suites test suites ($tests_per_suite tests per suite)" | tee -a test.log

	python CreatePerformanceTests.py $tests_per_suite $suites
	./test-runner.sh
	# This log.html file is created by Rebot and is a concatenation of all the results of all the parallel tests
	cp results_${today}/log.html ../performance_results/log_${tests}_${suites}.html
	echo password1 | sudo -S rm -rf test-cases/*

}

# Function to create load tests then run them, copy the results to a results diectory then tidy up afterwards
# Prameters:
# The number of tests to create
# The number of test suites used to run these tests
# The length of time the sut is to run for
# The number of cored the SUT is to run on
function create_load {
	tests=$1
  suites=$2
  timeout=$3
  cores=$4
	tests_per_suite=$(($tests/$suites))
	echo "`date`: Creating $tests tests in $suites test suites ($tests_per_suite tests per suite)" | tee -a test.log

	python CreateLoadTests.py $tests_per_suite $suites $timeout $cores
	./test-runner.sh
	cp results_${today}/log.html ../performance_results/log_${tests}_${suites}.html
	echo password1 | sudo -S rm -rf test-cases/*

}

# If today's results directory doesn't exist then create it

[[ -d results_${today} ]] && echo "results_${today} exists" || mkdir results_${today}