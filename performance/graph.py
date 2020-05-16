import csv
import glob

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# For this to work then the results files must be single line csv files containing the list of the times
# that each test took to run.

colours = ['','black','red','blue','green','cyan','magenta','yellow']
for f in glob.glob("perf*.csv"):
    xsize=0
    with open(f, "r") as t:
        d = csv.reader(t,quoting=csv.QUOTE_NONNUMERIC)
        data = np.array(list(d)[0][:-1])
        mult = int(f.split("-")[2].split("x")[0])
        print mult
        xsize=range(mult,len(data)*mult+1,mult)
    # plt.plot(xsize, data, 'o-', label=f, color=colours[mult])
    slope, intercept,r_value, p_value, std_err = stats.linregress(xsize,data)
    yfit = [slope*xi + intercept for xi in xsize]

    plt.plot(xsize,yfit, '-', label=f,color=colours[mult])

plt.title("Time to run a number of 5s API tests using docker containers")
plt.xlabel("total number of tests")
plt.ylabel("time in seconds")
plt.legend()
plt.show()
