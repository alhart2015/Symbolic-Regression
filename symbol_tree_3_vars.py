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

    def __eq__(self, other):
        '''
        Override for tree equality.

        Parameters:
            self - The tree
            other - The other tree

        Returns: True if the trees are identical, False otherwise
        '''
        return self.equality_helper(self.root, other.root)

    def equality_helper(self, node_1, node_2):
        '''
        Helper method for testing equality between two trees.

        Parameters:
            self - The tree. Not needed, but for clarity I'm keeping it as a
                class method, not making it a static one
            node_1 - A node on the first tree
            node_2 - A node on the second tree

        Returns: True if the trees are identical, False otherwise
        '''
        if node_1 and node_2 and node_1.operator == node_2.operator \
            and node_1.value == node_2.value:
            if not node_1.left and not node_1.right and \
                not node_2.left and not node_2.right:
                return True
            else:
                return self.equality_helper(node_1.left, node_2.left) and \
                    self.equality_helper(node_1.right, node_2.right)
        return False

    def __ne__(self, other):
        '''
        Override for inequality. You have to define __ne__ so that != behaves
        like you expect it to.

        Parameters:
            self - The tree
            other - The other tree

        Returns: the opposite of self == other
        '''
        return not self.__eq__(other)

    def mutate(self, node, rate, operations, terminals):
        '''
        Perform mutation on a tree.

        Parameters:
            self - The tree
            node - The node where mutation will take place
            rate - The chance that mutation happens at the given node
            operations - List of possible operations
            terminals - List of possible terminals
        '''
        r = random()
        if r < rate:
            if not node.operator:
                node.value = choice(terminals)
            else:
                node.operator = choice(operations)
        if node.left:
            self.mutate(node.left, rate, operations, terminals)
        if node.right:
            self.mutate(node.right, rate, operations, terminals)

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
            if r < chance or self_node.is_terminal():
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

        chance = 0.1
        other_selection = None
        other_node = other.root
        other_parent = other.root
        other_left = False

        while not other_selection:
            r = random()
            if r < chance or other_node.is_terminal():
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
            self.depth = depth
            self.fix_depth(node.left, depth+1)
            self.fix_depth(node.right, depth+1)

    def eval(self, x_val, y_val, z_val):
        '''
        Evaluate the tree, plugging x_val in for all x

        Parameters:
            self - The tree
            x_val - The value to be plugged in for all x in the tree
            y_val - The value to be plugged in for all y in the tree
            z_val - The value to be plugged in for all z in the tree

        Returns: the value of the tree
        '''
        return self.eval_helper(self.root, x_val, y_val, z_val)

    def eval_helper(self, node, x_val, y_val, z_val):
        '''
        Helper function for eval(). Calculates the value of the subtree rooted
        at this node with x_val plugged in for all x.

        Parameters:
            self - The tree
            node - The root of the subtree in question
            x_val - The value to be plugged in for all x in the tree
            y_val - The value to be plugged in for all y in the tree
            z_val - The value to be plugged in for all z in the tree

        Returns: the value of the subtree
        '''
        if not node.operator:   # at a leaf
            if node.value == 'x':
                return x_val
            elif node.value == 'y':
                return y_val
            elif node.value == 'z':
                return z_val
            else:
                return node.value
        else:                   # at an operator
            if node.operator == '+':
                node.value = self.eval_helper(node.left, x_val, y_val, z_val) +\
                    self.eval_helper(node.right, x_val, y_val, z_val)
                return node.value
            elif node.operator == '*':
                node.value = self.eval_helper(node.left, x_val, y_val, z_val) *\
                    self.eval_helper(node.right, x_val, y_val, z_val)
                return node.value
            else:   # division
                right = self.eval_helper(node.right, x_val, y_val, z_val)
                if right:   # you're not dividing by 0
                    node.value = self.eval_helper(node.left, x_val, y_val, z_val) / float(right)
                else:       # trying to divide by 0, just call it 1
                    node.value = 1
                return node.value

    def calc_error(self, x_vals, y_vals, z_vals, f_vals):
        '''
        Calculates the difference between the tree's function and the given data

        Parameters:
            self - The tree
            x_vals - A list of the x-values of the dataset
            y_vals - A list of the y-values of the dataset
            z_vals - A list of the z-values of the dataset
            f_vals - A list of the f-values of the dataset
        '''
        e = 0
        for i in xrange(len(x_vals)):
            e += abs(f_vals[i] - self.eval(x_vals[i], y_vals[i], z_vals[i]))
        self.error = e
        self.score = 1.0/(1+e)

    def return_error(self, x_vals, y_vals, z_vals, f_vals):
        '''
        Identical to above, except it returns the error and doesn't overwrite
        the field in the tree. Uses to compare training error to test error.

        Parameters:
            self - The tree
            x_vals - A list of the x-values of the dataset
            y_vals - A list of the y-values of the dataset
            z_vals - A list of the z-values of the dataset
            f_vals - A list of the f-values of the dataset

        Returns: The total error of the tree
        '''
        e = 0
        for i in xrange(len(x_vals)):
            e += abs(f_vals[i] - self.eval(x_vals[i], y_vals[i], z_vals[i]))

        return e



