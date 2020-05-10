from robot.api import SuiteVisitor


class RebotGetElapsedTests(SuiteVisitor):

    times = []
    # writes the start time and end time for each test
    def visit_test(self, test):
        with open("test_times.txt", "a") as t:
            print(test.starttime+"~"+test.endtime)
            t.write(test.starttime+"~"+test.endtime+"\n")

