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
    x = [1,2,3]
    y = [3,2,1]
    pop = Population(5, 4, 3, 0.1, 0.1, x, y)
    for t in pop.population:
        print t, t.eval(2), t.error, t.score

if __name__ == '__main__':
    main()