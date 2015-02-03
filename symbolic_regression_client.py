'''
Client code for symbolic regression algorithm. Uses genetic programming to find
the underlying functions for three sets of data.

Authors: Spencer Chadinha and Alden Hart
2/2/2015
'''

import subprocess as sub
from time import time
from op_node import OpNode

def get_generator_data(jar_name, x_vals):
    '''Collects data from a generator executable.

    Parameters: 
        jar_name - the name of the executable jar of the generating
            function
        x_vals - a list of the range of data to be collected. If these values
            are x, the function returns f(x)

    Returns: a list of the outpus of that function over the given range
    '''
    out = [None] * len(x_vals) # for efficiency's sake
    i = 0
    for x in x_vals:
        proc = sub.Popen(['java', '-jar', jar_name, str(x)],
                        stdout = sub.PIPE)
        (f_x, err) = proc.communicate()
        out[i] = f_x
        i += 1
        if i % 10 == 0:
            print i
    return out

def main():
    '''Main method for client code. Runs the symbolic regression algorithm.'''
    # BOUND = 5000
    # # x_vals = range(-BOUND, BOUND, 0.1)
    # x_vals = range(10*BOUND)
    # tic = time()
    # f1 = get_generator_data('Generator1.jar', x_vals)
    # print "That took", time() - tic, "seconds."

    node = OpNode("+", 0)
    node.left = OpNode("", 3)
    node.right = OpNode("", 4)
    print node.eval()

if __name__ == '__main__':
    main()