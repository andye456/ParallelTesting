#
# Test suite to run the end-point test in parallel using a varying number of Robot test cases per test.
# Runnig 50 tests from one Robot script is going to take 50*time for one test.
# Runnig 50 tests from two Robot scripts in parallel is going to take 25*time for one test
# This performance test will find out if running 50 tests from 50 Robot scripts in parallel is going to be 50x faster.
# And importantly the point at which performance gains tail off.
#
# CreatePerformanceTests.py creates a number of test cases each with their own docker-compose.yml
# and Dockerfile. The test cases are Robot scripts with a varying number of test cases in.
#

# A function to create the test cases and tidy up afterwards
. ./test-suite-utils.sh

# 50 tests 1 test suite
create 50 1

# 50 tests 2 test suites
create 50 2

# 50 tests 5 test suites
create 50 5

# 50 tests 10 test suites
create 50 10

# 50 tests 25 test suites
create 50 25

# 50 tests 50 test suites
create 50 50

