from robot.api import SuiteVisitor


class RebotGetElapsedTests(SuiteVisitor):

    times = []

    def visit_test(self, test):
        with open("test_times.txt", "a") as t:
            t.write(test.starttime+"~"+test.endtime+"\n")

