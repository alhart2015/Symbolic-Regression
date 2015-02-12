'''
Makes a sample set of data for us to test our shit with
'''

filename = "test_data.txt"

def f(x):
    return x**3 + 6*x - 4

with open(filename, 'w') as fle:
    step = 0.1
    x = -50
    for i in xrange(100):
        string = str(x) + " " + str(f(x)) + "\n"
        fle.write(string)
        x += step