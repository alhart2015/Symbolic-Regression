'''Class to represent an operator node in the tree

Authors: Spencer Chadinha and Alden Hart
2/2/2015
'''

class OpNode():
    """Class to represent an operator node in the tree.
    Supported operations: +, -, *, /, ^
    """

    def __init__(self, operator, value):
        self.operator = operator
        self.value = value
        self.left = None
        self.right = None
        self.depth = 1
        '''self.functions = {
            '+': 'add',
            '-': 'subtract',
            '*': 'multiply',
            '/': 'divide',
            '^': 'power'
        }
        try:
            self.func = getattr(self, self.functions[self.operator])
        except KeyError:
            self.func = None

    def eval(self, xVal):

        return self.eval_helper(self, xVal)

    def eval_helper(self, node, xVal):

        if not node.func:
            if node.value == 'x':
                return xVal
            else:
                return node.value

        left = node.eval_helper(node.left, xVal)
        right = node.eval_helper(node.right, xVal)
        node.value = node.func(left, right)
        return node.value'''

"""
    def add(self, l, r):
        '''Performs addition when the operator is +'''
        return l + float(r)

    def subtract(self, l, r):
        '''Performs subtraction when the operator is -'''
        return l - float(r)

    def multiply(self, l, r):
        '''Performs multiplication when the operator is x'''
        return l * float(r)

    def divide(self, l, r):
        '''Performs division when the operator is /'''
        if float(r) != 0:
            return l / float(r)
        else:
            return 1

    def power(self, l, r):
        '''Performs exponentation when the operator is ^'''
        return l ** float(r)
"""