'''
Client code for Symbolic Regression with genetic programming.

Authors: Spencer Chadinha and Alden Hart
2/11/2015
'''

from population_3_vars import Population
from random import random
from sys import maxint

def get_data(filename):
    '''
    Reads data from a file into lists.

    Parameter: filename - The name of the .txt file to read from
    Returns: A 4-tuple (x, y, z, f) where x, y, z are the input variables and
                f is f(x, y, z)
    '''
    x = []
    y = []
    z = []
    f = []
    with open(filename, 'r') as in_file:
        data = in_file.readlines()
        for line in data:
            # vals = line.split('\t')
            vals = line.split(' ')
            x.append(float(vals[0]))
            y.append(float(vals[1]))
            z.append(float(vals[2]))
            f.append(float(vals[3]))

    return x, y, z, f

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

def make_test_set(x, y, z, f, train_percent, test_percent):
    '''
    Splits x and y lists into training and test sets. The resulting training
    sets will use a random subset of the data.

    Parameters:
        x - The list of x-values
        y - The list of y-values
        percent - The percent of the data that will be used to train

    Returns: A list of length 8 where:
                list[0] = x_train
                list[1] = y_train
                list[2] = z_train
                list[3] = f_train
                list[4] = x_test
                list[5] = y_test
                list[6] = z_test
                list[7] = f_test
    '''
    x_train = []
    y_train = []
    z_train = []
    f_train = []
    x_test = []
    y_test = []
    z_test = []
    f_test = []
    for i in xrange(len(x)):
        r = random()
        if r < test_percent:
            x_train.append(x[i])
            y_train.append(y[i])
            z_train.append(z[i])
            f_train.append(f[i])
        elif r < train_percent:
            x_test.append(x[i])
            y_test.append(y[i])
            z_test.append(z[i])
            f_test.append(f[i])

    out = [x_train, y_train, z_train, f_train, x_test, y_test, z_test, f_test]

    return out

def experiment(population_size, depth_limit, terminal_bound, reproduction_rate,
                mutation_rate, x_train, y_train, z_train, f_train,
                x_test, y_test, z_test, f_test, num_generations):
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
                        reproduction_rate, mutation_rate, 
                        x_train, y_train, z_train, f_train)
        pop.evolve(num_generations)
        best = pop.best()
        print best, best.error
        winners.append(best)

    # Test them against the test set
    best_tree = winners[0]
    best_error = maxint
    for tree in winners:
        test_error = tree.return_error(x_test, y_test, z_test, f_test)
        if test_error < best_error:
            best_error = test_error
            best_tree = tree

    print "And the winner is...."
    print best_tree
    print "Training error:", best_tree.error
    print "Test error:", best_error

def main():

    x, y, z, f = get_data('data.txt')
    datasets = make_test_set(x, y, z, f, 0.05, 0.05)
    x_train = datasets[0]
    y_train = datasets[1]
    z_train = datasets[2]
    f_train = datasets[3]
    x_test = datasets[4]
    y_test = datasets[5]
    z_test = datasets[6]
    f_test = datasets[7]

    population_size = 500
    depth_limit = 5
    terminal_bound = 5
    reproduction_rate = 0.1
    mutation_rate = 0.1
    num_generations = 35

    experiment(population_size, depth_limit, terminal_bound, reproduction_rate,
        mutation_rate, x_train, y_train, z_train, f_train,
        x_test, y_test, z_test, f_test, num_generations)

    # big_x, big_y = get_data('G1Data.txt')
    # x, y = shrink_file(big_x, big_y)
    # x_train, y_train, x_test, y_test = make_test_set(x, y, 0.8)

    # # x = [1,2,3,4]
    # # y = [2,1,0,-1]
    # population_size = 1000
    # depth_limit = 10
    # terminal_bound = 5
    # reproduction_rate = 0.1
    # mutation_rate = 0.1
    # num_generations = 35
    # experiment(population_size, depth_limit, terminal_bound, reproduction_rate,
    #             mutation_rate, x_train, y_train, x_test, y_test, num_generations)
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
    
    