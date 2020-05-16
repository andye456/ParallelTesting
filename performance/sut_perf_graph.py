import csv
import glob

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# For this to work then the results files must be single line csv files containing the list of the times
# that each test took to run.

# Change this glob to change which set of results are used.
for f in glob.glob("results_2020-05-14/*-SUT-perf.csv"):
    xsize=0
    with open(f, "r") as t:
        d = csv.reader(t,quoting=csv.QUOTE_NONNUMERIC)
        data = np.array(list(d)[0][:55])
        mult = int(f.split("/")[1].split("-")[0])
        # This restricts the data to the first 55 values as the singe core process of the SUT is run 6 times.
        # i.e. once for every time the number of cores is increased.
        xsize=range(1, 56)
    plt.plot(xsize, data, 'o-',label="SUT running 100% on "+str(mult+1)+" cores")
    slope, intercept,r_value, p_value, std_err = stats.linregress(xsize,data)
    yfit = [slope*xi + intercept for xi in xsize]
    plt.plot(xsize,yfit, '--',)

plt.title("performance of SUT when parallel tests are run in the same container")
plt.ylabel("SUT performance")
plt.xlabel("Number of parallel tests")
# Add some vertical lines to divide the tests into the number of parallel containers used
x=0
for i in range(0,10):
    x=x+i
    plt.axvline(x+0.5,0,120,linestyle=':')
    plt.text(x+0.5,-1,i+1)

ax = plt.gca()
ax.axes.xaxis.set_ticks([])
ax.xaxis.set_label_coords(0.5, -0.05)
plt.legend()
plt.show()
