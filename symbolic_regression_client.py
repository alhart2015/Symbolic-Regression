'''
Client code for symbolic regression algorithm. Uses genetic programming to find
the underlying functions for three sets of data.

Authors: Spencer Chadinha and Alden Hart
2/2/2015
'''

import subprocess as sub
from time import time
from op_node import OpNode
from symbol_tree import SymbolTree

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

    # node = OpNode("+", 0)
    # l = OpNode("", 3)
    # r = OpNode("", 4)
    # node.left = l
    # node.right = r
    # print node.eval()

    n = OpNode("+", 0)
    t = SymbolTree(n)
    t.root.left = OpNode("", -1)
    t.root.left.depth = 2
    t.root.right = OpNode("*", 0)
    t.root.right.depth = 2
    t.root.right.left = OpNode("*", 0)
    t.root.right.left.depth = 3
    t.root.right.right = OpNode("", -3)
    t.root.right.right.depth = 3
    t.root.right.left.left = OpNode("", -3)
    t.root.right.left.left.depth = 4
    t.root.right.left.right = OpNode("", -3)
    t.root.right.left.right.depth = 4
    # t.root.left = OpNode("", 4)
    #t.root.right = OpNode("", 4)
    m = OpNode("/", 0)
    s = SymbolTree(m)
    s.root.left = OpNode("", -2)
    s.root.left.depth = 2
    s.root.right = OpNode("", 2)
    s.root.right.depth = 2
    
    print "p1"
    t.to_string()
    print "p2"
    s.to_string()
    t.crossover(s)
    #t.fix_depth(t.root, 1)
    #s.fix_depth(s.root, 1)
    print "c1"
    t.to_string()
    print "c2"
    s.to_string()

    print 
    #t.test_tree()
    print 
    #s.test_tree()

    # a = OpNode("", 3)
    # print a.func, a.value
    # if not a.func:
    #     print "osijo"

if __name__ == '__main__':
    main()