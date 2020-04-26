# test 1 50 tests 10 test suites
python CreatePerformanceTests.py 5 10
./test-runner.sh
cp output/log.html ../performance_results/log_50_10.html
# test 2 50 tests 25 test suites
python CreatePerformanceTests.py 2 25
./test-runner.sh
cp output/log.html ../performance_results/log_50_25.html
# test 3 50 tests 50 test suites
python CreatePerformanceTests.py 1 50
./test-runner.sh
cp output/log.html ../performance_results/log_50_50.html
sudo rm -rf test-cases/*
# test 4 10 tests 1 test suite
python CreatePerformanceTests.py 10 1
./test-runner.sh
cp output/log.html ../performance_results/log_10_1.html
sudo rm -rf test-cases/*
# test 5 10 tests 2 test suites
python CreatePerformanceTests.py 5 2
./test-runner.sh
cp output/log.html ../performance_results/log_10_2.html
sudo rm -rf test-cases/*
# test 6 10 tests 5 test suites
python CreatePerformanceTests.py 2 5
./test-runner.sh
cp output/log.html ../performance_results/log_10_5.html
sudo rm -rf test-cases/*
# test 7 10 tests 10 test suites
python CreatePerformanceTests.py 1 10
./test-runner.sh
cp output/log.html ../performance_results/log_10_10.html
sudo rm -rf test-cases/*


