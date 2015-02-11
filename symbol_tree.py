'''Class to represent a symbol tree.

Authors: Spencer Chadinha and Alden Hart
2/2/2015
'''

from random import random, randint
# from random import randint

class SymbolTree():
    """Class to represent a symbol tree."""
    def __init__(self, root):
        self.root = root
        self.score = 0      # Fitness score != squared error
        self.error = 0      # Squared error from the actual


    # def add_node(self, node):
    #     pass

    def to_string(self):
        """
        a rough visualization of a symbol tree, used to test tree operations
        """
        tree = []
        tree.append(self.root)
        printout = []

        while len(tree) > 0:
            n = tree.pop(0)

            if n.left != None:
                tree.append(n.left)
            if n.right != None:
                tree.append(n.right)

            if n.depth > len(printout):
                l = []
                printout.append(l)

                if n.operator == "":
                    printout[n.depth-1].append(n.value)
                else:
                    printout[n.depth-1].append(n.operator)
            else:
                if n.operator == "":
                    printout[n.depth-1].append(n.value)
                else:
                    printout[n.depth-1].append(n.operator)   

        for i in range(len(printout)):
            print printout[i]   


    def mutate(self, node, potential, current, rate, operations, terminals):

        if (current < potential) and node:
            # print "valid mutation node"
            r = random()
            if r < rate:
                # print "within the rate, " + str(rate)
                if node.operator == "":
                    # print "mutating value node"
                    past = node.value
                    while node.value == past:
                        node.value = terminals[randint(0, len(terminals)-1)]
                    # print "old: " + str(past) + " new: " + str(node.value)
                else:
                    # print "mutating operator node"
                    past = node.operator
                    while node.operator == past:
                        node.operator = operations[randint(0, len(operations)-1)]
                    # print "old: " + str(past) + " new: " + str(node.operator)
                current += 1
            nxt = random()
            if nxt < .5:
                self.mutate(node.left, potential, current, rate, operations, terminals)
            else:
                self.mutate(node.right, potential, current, rate, operations, terminals)

    def crossover(self, other):
        """ Unfinished crossing over method. there is an issue when assigning
        the parent to the value of the selected node
        """
        self_selection = None
        self_node = self.root
        self_parent = self.root
        self_left = False
        chance = .1

        while self_selection == None:
            r = random()
            if r < chance or self_node.operator == "":
                self_selection = self_node
            else:
                nxt = random()
                chance += .2
                self_parent = self_node
                if nxt < .5:
                    self_left = True
                    self_node = self_node.left
                else:
                    self_left = False
                    self_node = self_node.right
            

        other_selection = None
        other_node = other.root
        other_parent = other.root
        other_left = False
        chance = .1 

        while other_selection == None:
            r = random()
            if r < chance or other_node.operator == "":
                other_selection = other_node
            else:
                nxt = random()
                chance += .2
                other_parent = other_node
                if nxt < .5:
                    other_left = True
                    other_node = other_node.left
                else:
                    other_left = False
                    other_node = other_node.right

        if self_left:
            if other_left:
                temp = self_parent.left
                #self._fix_depth(self_parent.left, other_parent.left.depth)
                #self._fix_depth(other_parent.left, temp.depth)
                self_parent.left = other_parent.left
                other_parent.left = temp
            else:
                temp = self_parent.left
                #self._fix_depth(self_parent.left, other_parent.right.depth)
                #self._fix_depth(other_parent.right, temp.depth)
                self_parent.left = other_parent.right
                other_parent.right = temp
        else:
            if other_left:
                temp = self_parent.right
                #self._fix_depth(self_parent.right, other_parent.left.depth)
                #self._fix_depth(other_parent.left, temp.depth)
                self_parent.right = other_parent.left
                other_parent.left = temp
            else:
                temp = self_parent.right
                #self._fix_depth(self_parent.right, other_parent.right.depth)
                #self._fix_depth(other_parent.right, temp.depth)
                self_parent.right = other_parent.right
                other_parent.right = temp
        self.fix_depth(self.root, 1)
        other.fix_depth(other.root, 1)

    def fix_depth(self, node, depth):
        if node:
            node.depth = depth
            self.fix_depth(node.left, depth+1)
            self.fix_depth(node.right, depth+1)


    def eval(self, xVal):
        # When the function contains 'X' as a variable we need a way to
        # change X into any number we want, so I added xVal as the 
        # value we want X to be when the function is evaluated
        '''Evaluates the subtree rooted at this node

        Returns: the value of the subtree rooted at this node
        '''
        self.to_string()
        return self.eval_helper(self.root, xVal)

    def eval_helper(self, node, xVal):
        '''Recursive helper to evaluate the subtree rooted at the node'''
        # Added the if/else statement to determine when to use the xVal
        # variable
        '''if not node.func:
            if node.value == 'x':
                return xVal
            else:
                return node.value'''

        '''left = node.eval_helper(node.left, xVal)
        print node.operator
        right = node.eval_helper(node.right, xVal)
        node.value = node.func(left, right)
        return node.value'''

        if node.operator == "":
            if node.value == 'x':
                return xVal
            else:
                return node.value
        else:
            if node.operator == "+":
                node.value = self.eval_helper(node.left, xVal) +\
                 self.eval_helper(node.right, xVal)
                return node.value
            elif node.operator == "-":
                node.value = self.eval_helper(node.left, xVal) -\
                 self.eval_helper(node.right, xVal)
                return node.value
            elif node.operator == "*":
                node.value = self.eval_helper(node.left, xVal) *\
                 self.eval_helper(node.right, xVal)
                return node.value
            elif node.operator == "^":
                exp = self.eval_helper(node.right, xVal)
                exp = int(abs(exp))
                # print self.eval_helper(node.left, xVal), exp
                node.value = self.eval_helper(node.left, xVal) ** exp
                return node.value
            else:
                right = self.eval_helper(node.right, xVal)
                if right != 0:
                    node.value = self.eval_helper(node.left, xVal) /\
                     float(self.eval_helper(node.right, xVal))
                else:
                    node.value = 1
                return node.value

    def test_tree_help(self, node, lvl):
        # print "node: " + node.operator + " " + str(node.value) + " level: " + str(lvl)
        #if node.left:
            # print "left child: " + node.left.operator + " " + str(node.left.value)
            # print "thinks its at depth: " + str(node.left.depth) 
        #if node.right:
            # print "right child: " + node.right.operator + " " + str(node.right.value)
            # print "thinks its at depth: " + str(node.right.depth)
        # print

        if node.left:
            self.test_tree_help(node.left, lvl+1)
        if node.right:
            self.test_tree_help(node.right, lvl+1)

    def test_tree(self):
        self.test_tree_help(self.root, 1)

    # def add(self, l, r):
    #     '''Performs addition when the operator is +'''
    #     return l + r

    # def subtract(self, l, r):
    #     '''Performs subtraction when the operator is -'''
    #     return l - r

    # def multiply(self, l, r):
    #     '''Performs multiplication when the operator is x'''
    #     return l * r

    # def divide(self, l, r):
    #     '''Performs division when the operator is /'''
    #     if float(r) != 0:
    #         return l / float(r)
    #     else:
    #         return 1

    # def power(self, l, r):
    #     '''Performs exponentation when the operator is ^'''
    #     return l ** r
