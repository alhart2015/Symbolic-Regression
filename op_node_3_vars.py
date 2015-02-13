'''
Class to represent a node in a symbol tree.

Authors: Spencer Chadinha and Alden Hart
2/12/2015
'''

class OpNode():
    '''
    Class to represent a node in the symbol tree.
    '''

    def __init__(self, operator, value):
        self.operator = operator
        self.value = value
        self.left = None
        self.right = None
        self.depth = 1

    def __str__(self):
        return str(self.operator) + " " + str(self.value)

    def is_terminal(self):
        '''
        Helper to indicate whether a node is a terminal or not.

        Returns: true if the node is a terminal, false otherwise
        '''
        return self.operator == ""
        