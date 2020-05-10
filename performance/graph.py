import csv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

data = []
# read the results file
with open("test_times.csv", "r") as t:
    d = csv.reader(t,quoting=csv.QUOTE_NONNUMERIC)
    data = list(d)[0]

# y = [2.2,5.122, 7.842, 13.045, 20.012]
# x = [1,2,3,4,5]
x = list(range(1, 51))

print(str(data))
print(str(x))

plt.title("Time to run a number of 5s API tests using docker containers")
plt.plot(x, data[:-1], 'ro-')
plt.xlabel("number of tests run in parallel")
plt.ylabel("time in seconds")
plt.show()