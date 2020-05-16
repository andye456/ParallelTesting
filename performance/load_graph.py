import csv
import glob

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# For this to work then the results files must be single line csv files containing the list of the times
# that each test took to run.

colours = ['','black','red','blue','green','cyan','magenta','yellow']
# Change this date and glob as appropriate
for f in glob.glob("results_2020-05-14/load*.csv"):
    xsize=0
    with open(f, "r") as t:
        d = csv.reader(t,quoting=csv.QUOTE_NONNUMERIC)
        data = np.array(list(d)[0][:-1])
        mult = int(f.split("-")[6].split(".")[0])
        xsize=range(1, 11)
    plt.plot(xsize, data, 'o-', label="load on "+str(mult)+" cores", color=colours[mult])
    slope, intercept,r_value, p_value, std_err = stats.linregress(xsize,data)
    yfit = [slope*xi + intercept for xi in xsize]
    plt.plot(xsize,yfit, '--', label="average load on "+str(mult)+" cores",color=colours[mult])

plt.title("Time taken to run 1-10 tests in parallel, each running one 2 minute load test using an increasing number of cores")
plt.xlabel("number of parallel tests")
plt.ylabel("time in seconds")
plt.legend()
plt.show()
