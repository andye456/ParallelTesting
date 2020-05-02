# A function to create the test cases and tidy up afterwards
function create {
	tests=$1
  suites=$2
	tests_per_suite=$(($tests/$suites))
	echo "`date`: Creating $tests tests in $suites test suites ($tests_per_suite tests per suite)" | tee -a test.log

	python CreatePerformanceTests.py $tests_per_suite $suites
	./test-runner.sh
	cp output/log.html ../performance_results/log_${tests}_${suites}.html
	echo password1 | sudo -S rm -rf test-cases/*
}


