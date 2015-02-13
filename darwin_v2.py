'''
Client code for Symbolic Regression with genetic programming.

Authors: Spencer Chadinha and Alden Hart
2/11/2015
'''

from population import Population
from random import random
from sys import maxint

def get_data(filename):
    '''
    Reads data from a file into lists.

    Parameter: filename - The name of the .txt file to read from
    Returns: two lists, one with the x-values of the data and one with the 
        y-values
    '''
    x = []
    y = []
    with open(filename, 'r') as f:
        data = f.readlines()
        for line in data:
            vals = line.split('\t')
            # vals = line.split(' ')
            x.append(float(vals[0]))
            y.append(float(vals[1]))

    return x, y

def shrink_file(x_vals, y_vals):
    '''
    Shrinks the file as described above.

    Parameters:
        x_vals - The old, huge list of x-values
        y_vals - The old, huge list of y-values

    Returns: A tuple (new_x, new_y) of the new, smaller lists of data
    '''

    if len(x_vals) < 10000:
        print "This is too small to shrink."
        return

    middle = len(x_vals)/2
    new_size = 1000
    half_size = new_size/2
    new_start = middle - half_size
    new_end = middle + half_size

    new_x = []
    new_y = []
    for i in xrange(new_start, new_end):
        new_x.append(x_vals[i])
        new_y.append(y_vals[i])

    return new_x, new_y

def make_test_set(x, y, percent):
    '''
    Splits x and y lists into training and test sets. The resulting training
    sets will use a random subset of the data.

    Parameters:
        x - The list of x-values
        y - The list of y-values
        percent - The percent of the data that will be used to train

    Returns: A 4-tuple (x_train, y_train, x_test, y_test)
    '''
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    for i in xrange(len(x)):
        r = random()
        if r < percent:
            x_train.append(x[i])
            y_train.append(y[i])
        else:
            x_test.append(x[i])
            y_test.append(y[i])

    return x_train, y_train, x_test, y_test

def experiment(population_size, depth_limit, terminal_bound, reproduction_rate,
                mutation_rate, x_train, y_train, x_test, y_test, num_generations):
    '''
    Performs the experiment. Will run GP 10 times, getting a best tree each
    time. It will then evaluate each tree on the test set and return the
    best overall tree.
    '''
    NUM_TRIES = 10
    winners = []
    # Run it 10 times to get ten good trees
    for i in xrange(NUM_TRIES):
        print "ATTEMPT", i+1
        pop = Population(population_size, depth_limit, terminal_bound, 
                        reproduction_rate, mutation_rate, x_train, y_train)
        pop.evolve(num_generations)
        best = pop.best()
        print best, best.error
        winners.append(best)

    # Test them against the test set
    best_tree = winners[0]
    best_error = maxint
    for tree in winners:
        test_error = tree.return_error(x_test, y_test)
        print tree
        print tree.error, test_error
        if test_error < best_error:
            best_error = test_error
            best_tree = tree

    print "And the winner is...."
    print best_tree
    print "Training error:", best_tree.error
    print "Test error:", best_error

def main():
    big_x, big_y = get_data('G1Data.txt')
    x, y = shrink_file(big_x, big_y)
    x_train, y_train, x_test, y_test = make_test_set(x, y, 0.8)

    # x = [1,2,3,4]
    # y = [2,1,0,-1]
    population_size = 1000
    depth_limit = 10
    terminal_bound = 5
    reproduction_rate = 0.1
    mutation_rate = 0.1
    num_generations = 35
    experiment(population_size, depth_limit, terminal_bound, reproduction_rate,
                mutation_rate, x_train, y_train, x_test, y_test, num_generations)
    # pop = Population(population_size, depth_limit, 
    #                 terminal_bound, reproduction_rate,
    #                 mutation_rate, x, y)
    # # pop.print_population()
    # pop.evolve(num_generations)
    # best = pop.best()
    # print best, best.error
    # print pop.population[-1], pop.population[-1].error
    # pop.print_population()
    # print pop.diversity()
    # worst = pop.population[-1]
    # print worst, worst.error, worst.score

if __name__ == '__main__':
    main()
    
    