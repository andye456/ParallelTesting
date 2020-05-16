"""
Produces load on CPU cores for a specified amount of time and a specified number of cores
"""
import datetime
import sys
from multiprocessing import Pool
from multiprocessing import cpu_count
#import signal

def exit_chld(x, y):
    global stop_loop
    stop_loop = 1


def f(x):
    start = int(datetime.datetime.now().strftime("%s"))
    start_ext = datetime.datetime.now().strftime("%Y%m%dT%H-%M-%S.%f")
    now = int(datetime.datetime.now().strftime("%s"))
    c=x
    while not do_load.stop_loop and now - start < int(do_load.runtime):
        x = x + 0.00001
        now = int(datetime.datetime.now().strftime("%s"))
    # Create a text file with the count that was reached - this will be running in /SUT in Docker container

    with open("/SUT/output/"+str(c)+"-"+start_ext+".txt", "w") as fl:
        print("Writing SUT time to file.....")
        fl.write(str(x))

class do_load:
    stop_loop = 0
    runtime = 0
    cores = 0
    exit_chld(1,2)
    def __init__(self, runtime, cores):
        do_load.runtime=runtime
        do_load.cores=cores
        processes = cpu_count()
        print('-' * 20)
        print('Running load on CPU(s)')
        print('Utilizing %s cores' % do_load.cores)
        print('running for %s seconds' % do_load.runtime)
        print('-' * 20)
        pool = Pool(processes)
        pool.map(f, range(int(do_load.cores)))


if __name__ == '__main__':
    d = do_load(sys.argv[1],sys.argv[2])
    # signal.signal(signal.SIGINT, exit_chld)
