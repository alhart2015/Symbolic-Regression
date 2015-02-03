'''Class to represent an operator node in the tree

Authors: Spencer Chadinha and Alden Hart
2/2/2015
'''

class OpNode():
    """Class to represent an operator node in the tree.
    Supported operations: +, -, x, /, ^
    """

    def __init__(self, operator, value):
        self.operator = operator
        self.value = value
        self.left = None
        self.right = None
        self.functions = {
            '+': 'add',
            '-': 'subtract',
            'x': 'multiply',
            '/': 'divide',
            '^': 'power'
        }
        try:
            self.func = getattr(self, self.functions[self.operator])
        except KeyError:
            self.func = None

    def eval(self):
        '''Evaluates the subtree rooted at this node

        Returns: the value of the subtree rooted at this node
        '''
        return self.eval_helper(self)

    def eval_helper(self, node):
        '''Recursive helper to evaluate the subtree rooted at the node'''
        if not node.func:
            return node.value

        left = node.eval_helper(node.left)
        right = node.eval_helper(node.right)
        node.value = node.func(left, right)


    def add(self, l, r):
        '''Performs addition when the operator is +'''
        return l + r

    def subtract(self, l, r):
        '''Performs subtraction when the operator is -'''
        return l - r

    def multiply(self, l, r):
        '''Performs multiplication when the operator is x'''
        return l * r

    def divide(self, l, r):
        '''Performs division when the operator is /'''
        return l / float(r)

    def power(self, l, r):
        '''Performs exponentation when the operator is ^'''
        return l ** r