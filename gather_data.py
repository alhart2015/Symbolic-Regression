'''
Makes .txt files for Generator1 and Generator2 data. They are very, very
slow to run, so I'm just gonna run this overnight and get it over with.
'''

import subprocess as sub
from time import time

def run(jar_name, arg):
    '''Runs a jar with the given arguments

    Parameters:
        jar_name - the name of the jar to be executed
        arg - the argument to pass to the jar

    Returns: the output of the jar as a string
    '''

    proc = sub.Popen(['java', '-jar', jar_name, str(arg)],
                        stdout = sub.PIPE)
    (out, err) = proc.communicate()
    return out

BOUND = 5
SIZE = 20*BOUND
STEP_SIZE = 0.1

def main():
    '''Runs each generator 100,000 times in the range [-5,000, 5,000]
    with step size 0.1 and stores it to txt files
    '''
    x_vals = [None] * SIZE
    y1_vals = [None] * SIZE
    y2_vals = [None] * SIZE
    x = -BOUND
    start = time()
    for i in xrange(SIZE):
        x_vals[i] = x
        y1_vals[i] = run("Generator1.jar", x)
        y2_vals[i] = run("Generator2.jar", x)
        x += STEP_SIZE
    print "Finished generating values. Time:", time() - start
    io_start = time()
    f1 = open("G1Data.txt", "wb")
    f2 = open("G2Data.txt", "wb")
    for i in xrange(SIZE):
        data_1 = str(x_vals[i]) + "\t" + str(y1_vals[i])
        data_2 = str(x_vals[i]) + "\t" + str(y2_vals[i])
        f1.write(data_1)
        f2.write(data_2)
    f1.close()
    f2.close()
    print "Finished writing files. IO Time:", time() - io_start
    print "Total time:", time() - start

if __name__ == '__main__':
    main()
            