'''
Cut the generator data from 100,000 datapoints ranging from -5000,5000 to 1,000
datapoints from -50,50. This is the only interesting range of the function.

Author: Alden Hart
2/12/2015
'''

def shrink_file(x_vals, y_vals):
    '''
    Shrinks the file as described above.

    Parameters:
        x_vals - The old, huge list of x-values
        y_vals - The old, huge list of y-values

    Returns: A tuple (new_x, new_y) of the new, smaller lists of data
    '''
    middle = len(x_vals)/2
    new_size = 1000
    half_size = new_size/2
    new_start = middle - half_size
    new_end = middle + half_size

    new_x = []
    new_y = []
    t = 0
    for i in xrange(new_start, new_end):
        new_x[t] = x_vals[i]
        new_y = y_vals[i]
        t += 1

    return new_x, new_y
