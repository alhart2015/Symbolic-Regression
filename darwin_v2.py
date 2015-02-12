'''
Client code for Symbolic Regression with genetic programming.

Authors: Spencer Chadinha and Alden Hart
2/11/2015
'''

from population import Population

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
            vals = line.split(' ')
            x.append(float(vals[0]))
            y.append(float(vals[1]))

    return x, y


def main():
    # x, y = get_data('test_data.txt')
    x = [1,2,3,4]
    y = [2,1,0,-1]
    population_size = 10
    depth_limit = 10
    terminal_bound = 3
    reproduction_rate = 0.1
    mutation_rate = 0.1
    num_generations = 35
    pop = Population(population_size, depth_limit, 
                    terminal_bound, reproduction_rate,
                    mutation_rate, x, y)
    # pop.print_population()
    pop.evolve(num_generations)
    best = pop.best()
    print best, best.error, best.score
    pop.print_population()
    print pop.diversity
    # worst = pop.population[-1]
    # print worst, worst.error, worst.score

if __name__ == '__main__':
    main()
    