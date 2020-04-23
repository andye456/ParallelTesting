from robot.api import SuiteVisitor
import os
from datetime import datetime
from dateutil import parser


class RebotGetElapsedSuite(SuiteVisitor):
    # reads the start and end timestamps to get the tru elapsed time for the testsuite.

    start_times = []
    end_times = []

    def visit_suite(self, suite):
        with open("test_times.txt", "rt") as f:
            for dts in f:
                print(dts)
                start = parser.parse(dts.split("~")[0])
                print("start = " + str(start))
                end = parser.parse(dts.split('~')[1])
                print("end = " + str(end))
                self.start_times.append(start)
                self.end_times.append(end)

        first = min(self.start_times)
        last = max(self.end_times)
        print(first.strftime("%Y%m%d %H:%M:%S.%f"))
        print(last.strftime("%Y%m%d %H:%M:%S.%f"))
        suite.starttime=first.strftime("%Y%m%d %H:%M:%S.%f")
        suite.endtime=str(last.strftime("%Y%m%d %H:%M:%S.%f"))
        os.remove("test_times.txt")
