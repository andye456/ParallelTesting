from robot.api import SuiteVisitor
import os
from datetime import datetime
from dateutil import parser


class RebotGetElapsedSuite(SuiteVisitor):
    # reads the start and end timestamps to get the true elapsed time for the test suite.

    start_times = []
    end_times = []

    # Puts all of the start times into start_times array and end times into end_times array
    # Finds the minimum start time in start_times and the maximum end time in end_times
    # Finds the difference between the 2 to get the elapsed time.
    def visit_suite(self, suite):
        with open("test_times.txt", "rt") as f:
            for dts in f:
                print(">>>"+dts)
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
        suite.endtime=last.strftime("%Y%m%d %H:%M:%S.%f")
        # Also outputs the elapsed time to a file in csv format and for input into matplotlib
        elapsed = (last - first).total_seconds()
        print("elapsed = "+str(elapsed))
        with open("test_times.csv", "a") as t:
            t.write(str(elapsed)+",")
        os.remove("test_times.txt")
