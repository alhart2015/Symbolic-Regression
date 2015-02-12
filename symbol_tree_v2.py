'''
Class to represent a symbol tree.

Authors: Spencer Chadinha and Alden Hart
'''

from collections import deque
from random import random, choice

class SymbolTree():

    def __init__(self, root):
        self.root = root
        self.score = 0      # Fitness score, not error
        self.error = 0      # Error from the actual values
        self.depth = 0

    def __str__(self):
        '''
        Make trees printable.
        '''
        tree = deque()
        tree.append(self.root)
        printout = []

        while tree:
            n = tree.pop()
            if n.left:
                tree.appendleft(n.left)
            if n.right:
                tree.appendleft(n.right)

            if n.depth > len(printout):
                l = []
                printout.append(l)

                if not n.operator:  # leaf node
                    printout[n.depth-1].append(n.value)
                else:
                    printout[n.depth-1].append(n.operator)
            else:
                if not n.operator:  # leaf node
                    printout[n.depth-1].append(n.value)
                else:
                    printout[n.depth-1].append(n.operator)

        out = ""
        for lst in printout:
            for term in lst:
                out += str(term)
                out += " "
            out += "\n"

        return out

    def mutate(self, node, potential, current, rate, operations, terminals):
        '''
        Perform mutation on a tree.

        Parameters:
            self - The tree
            node - The node where mutation will take place
            potential - The total number of mutations you're willing to let
                happen
            current - The number of mutations that have already happened in this
                tree
            rate - The chance that mutation happens at the given node
            operations - List of possible operations
            terminals - List of possible terminals
        '''
        if (current < potential) and node:
            r = random()
            if r < rate:
                if not node.operator:
                    past = node.value
                    while node.value == past:
                        node.value = choice(terminals)
                    else:
                        past = node.operator
                        while node.operator == past:
                            node.operator = choice(operations)
                    current += 1

                nxt = random()
                LEFT = 0.5
                if nxt < LEFT:
                    self.mutate(node.left, potential, current, rate, operations, terminals)
                else:
                    self.mutate(node.right, potential, current, rate, operations, terminals)

    def crossover(self, other):
        '''
        Performs the crossover between two trees.

        Parameters:
            self - The tree
            other - The other tree to be crossed with
        '''
        chance = 0.1
        incr = 0.2
        LEFT = 0.5

        self_selection = None
        self_node = self.root
        self_parent = self.root
        self_left = False

        while not self_selection:
            r = random()
            if r < chance or not self_node.operator:
                self_selection = self_node
            else:
                nxt = random()
                chance += incr
                self_parent = self_node
                if nxt < LEFT:
                    self_left = True
                    self_node = self_node.left
                else:
                    self_node = self_node.right

        other_selection = None
        other_node = other.root
        other_parent = other.root
        other_left = False

        while not other_selection:
            r = random()
            if r < chance or not other_node.operator:
                other_selection = other_node
            else:
                nxt = random()
                chance += incr
                other_parent = other_node
                if nxt < LEFT:
                    other_left = True
                    other_node = other_node.left
                else:
                    other_node = other_node.right

        if self_left:
            if other_left:  # both left
                temp = self_parent.left
                self_parent.left = other_parent.left
                other_parent.left = temp
            else:           # self_left, other_right
                temp = self_parent.left
                self_parent.left = other_parent.right
                other_parent.right = temp
        else:
            if other_left:  # self_right, other_left
                temp = self_parent.right
                self_parent.right = other_parent.left
                other_parent.left = temp
            else:           # both right
                temp = self_parent.right
                self_parent.right = other_parent.right
                other_parent.right = temp
        self.fix_depth(self.root, 1)
        other.fix_depth(other.root, 1)

    def fix_depth(self, node, depth):
        '''
        Reset the depth of each node in the tree

        Parameters:
            self - The tree
            node - The node you're at in the tree
            depth - The depth you're at in the tree
        '''
        if node:
            node.depth = depth
            tree.depth = depth
            self.fix_depth(node.left, depth+1)
            self.fix_depth(node.right, depth+1)

    def eval(self, x_val):
        '''
        Evaluate the tree, plugging x_val in for all x

        Parameters:
            self - The tree
            x_val - The value to be plugged in for all x in the tree

        Returns: the value of the tree
        '''
        return self.eval_helper(self.root, x_val)

    def eval_helper(self, node, x_val):
        '''
        Helper function for eval(). Calculates the value of the subtree rooted
        at this node with x_val plugged in for all x.

        Parameters:
            self - The tree
            node - The root of the subtree in question
            x_val - The value to be plugged in for all x in the tree

        Returns: the value of the subtree
        '''
        if not node.operator:   # at a leaf
            if node.value == 'x':
                return x_val
            else:
                return node.value
        else:                   # at an operator
            if node.operator == '+':
                node.value = self.eval_helper(node.left, x_val) +\
                    self.eval_helper(node.right, x_val)
                return node.value
            elif node.operator == '*':
                node.value = self.eval_helper(node.left, x_val) *\
                    self.eval_helper(node.right, x_val)
                return node.value
            else:   # division
                right = self.eval_helper(node.right, x_val)
                if right:   # you're not dividing by 0
                    node.value = self.eval_helper(node.left, x_val) / float(right)
                else:       # trying to divide by 0, just call it 1
                    node.value = 1
                return node.value

    def calc_error(self, x_vals, y_vals):
        '''
        Calculates the difference between the tree's function and the given data

        Parameters:
            self - The tree
            x_vals - A list of the x-values of the dataset
            y_vals - A list of the y-values of the dataset
        '''
        e = 0
        for i in xrange(len(x_vals)):
            e += abs(y_vals[i] - self.eval(x_vals[i]))
        self.error = e
        self.score = 1.0/(1+e)

