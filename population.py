'''
Class to represent a population of SymbolTrees.

Authors: Spencer Chadinha and Alden Hart
2/11/2015
'''

from op_node_v2 import OpNode
from symbol_tree_v2 import SymbolTree
from random import random, choice, sample
from copy import deepcopy

class Population():
    '''
    Class representing a population of SymbolTrees. This class will contain
    methods for making the population, making the next generation...
    '''

    def __init__(self, size, depth_limit, terminal_bound, rep, mutate, x, y):
        '''
        Constructor for the population object.

        Parameters:
            self - The population
            size - The number of trees in the population
            depth_limit - The limit on how deep trees are at the beginning,
                before crossover
            terminal_bound - The bound on the set of terminals
            rep - The rate of reproduction
            mutate - The rate of mutation
            x - The x-values of the function you're evaluating
            y - The y-values of the function you're evaluating
        '''
        self.size = size                        # number of trees in the 
                                                # population
        self.operators = ['+', '*', '/']        # valid operators
        # valid terminals
        self.terminals = make_terminals(-terminal_bound, terminal_bound)
        self.depth_limit = depth_limit          # initial depth limit of 
                                                # all the trees
        self.reproduction_rate = rep
        self.mutation_rate = mutate
        self.population = []
        self.total_score = 0
        self.diversity = 0
        self.x_vals = x
        self.y_vals = y
        self.populate()

    def populate(self):
        '''
        Initializer method. Fills the Population object with randomly generated
        SymbolTrees

        Parameters: self - The population of trees
        '''
        cutoff = 0.5
        for i in xrange(self.size):
            op = self.random_operator()
            node = OpNode(op, 0)
            t = SymbolTree(node)
            self.add_children(cutoff, 1, t.root)
            self.population.append(t)
            t.calc_error(self.x_vals, self.y_vals)
            self.total_score += t.score
        self.population.sort(key=lambda t: t.score, reverse=True)
        self.diversity = self.compare_all()


    def random_operator(self):
        '''
        Helper function to return a random operator from the set of valid ones.

        Parameters: self - The population

        Returns: A string representing the operator
        '''
        return choice(self.operators)

    def random_terminal(self):
        '''
        Helper function to return a random terminal from the set of valid ones.

        Parameters: self - The population

        Returns: A valid terminal
        '''
        return choice(self.terminals)

    def add_children(self, cutoff, at, node):
        '''
        Adds children to the given tree at the given node recursively. Generates
        a random symbol tree given the starting node, a percent chance of
        generating a terminal node, a maximum depth limit, and a set of terminal
        and operator values.

        Parameters:
            self - The population
            cutoff - The probability with which you add a terminal node
            at - The current depth of the function
            node - The node at the root of the subtree you're adding to
        '''
        check_left = random()
        check_right = random()

        # Check if your random number says you should generate a terminal
        # on the left. Also generate a terminal if you're too deep in the tree.
        if check_left < cutoff or at > self.depth_limit:
            left = OpNode("", self.random_terminal())
            left.depth = at + 1
            node.left = left
        else:   # Make an operator node
            left = OpNode(self.random_operator(), 0)
            left.depth = at + 1
            node.left = left
            self.add_children(cutoff, at+1, left)

        # Check if your other random number says you should generate a terminal
        # on the right. Also generate a terminal if you're too deep.
        if check_right < cutoff or at > self.depth_limit:
            right = OpNode("", self.random_terminal())
            right.depth = at + 1
            node.right = right
        else:   # Make an operator node
            right = OpNode(self.random_operator(), 0)
            right.depth = at + 1
            node.right = right
            self.add_children(cutoff, at+1, right)

    def next_gen(self):
        '''
        Generates the next generation of trees from our population.

        Parameters: self - The population
        '''
        new_gen = []
        possible_mutations = 1
        node_mutation_rate = 0.5

        # Copy the best existing members into the next generation. This
        # is called reproduction
        for i in xrange(int(self.size * self.reproduction_rate) + 1):
            new_gen.append(self.population[i])

        # Mutate a random tree
        for i in xrange(int(self.size * self.mutation_rate) + 1):
            t = choice(self.population)
            t.mutate(t.root, possible_mutations, 0, node_mutation_rate,
                     self.operators, self.terminals)

        # Crossover for the rest of the new generation
        while len(new_gen) < self.size:
            p1 = self.select_individual()
            p2 = self.select_individual()

            # Gotta make copies to prevent overwriting bugs
            copy1 = deepcopy(p1)
            copy2 = deepcopy(p2)
            copy1.crossover(copy2)
            new_gen.append(copy1)

        new_gen.sort(key=lambda t: t.score, reverse=True)
        self.population = new_gen
        self.diversity = self.compare_all()

    def select_individual(self):
        '''
        Selects a member of the population to cross over. Probabilistically
        selects fitter trees more often.

        Parameters: self - The population

        Returns: The selected SymbolTree
        '''
        return self.tournament_selection(self.size/10)

    def tournament_selection(self, size):
        '''
        Performs tournament_selection to select an individial for crossing over.
        In tournament selection, you randomly select a subset of the population
        and pick the single fittest individual from that subset.

        Parameters: 
            self - The population
            size - The number of individuals to be randomly picked

        Returns: The fittest tree from the tournament
        '''
        tourney = sample(self.population, size)
        best_score = 0
        for t in tourney:
            if t.score > best_score:
                best_score = t.score
                best_tree = t

        return best_tree

    def best(self):
        '''
        Returns the most fit individial in that population

        Parameters: self - The population

        Returns: The most fit tree in the population
        '''
        return self.population[0]

    def evolve(self, num_generations):
        '''
        Run genetic programming for the given number of generations.

        Parameters:
            self - The population
            num_generations - The number of generations to let it run for
        '''
        for i in xrange(num_generations):
            self.next_gen()

    def print_population(self):
        '''
        Method for testing. Print out the whole population.

        Parameters: self - The population
        '''
        for i in xrange(self.size):
            tree = self.population[i]
            print tree, tree.error, tree.score

    def compare_all(self):
        '''
        Compares all trees in the population to give the diversity of the
        population. NOTE: this is implemented with a list, not a set. The
        reason for this is that trees can change during their lifetime,
        and in order to put them in a set they have to be hashable. I'm
        not sure this matters in practice, as they won't be changed while
        the set is around, but I'm erring on the side of caution here.

        Parameters: self - The population

        Returns: a tuple, (count, pct). Count is the number of unique trees
            in the population, pct is the percentage of the population that
            is unique. This is a reasonable measure for the overall
            diversity of the population.
        '''
        unique = []
        is_unique = True
        count = 0
        for i in xrange(self.size):
            for tree in unique:
                if self.population[i] == tree:
                    is_unique = False
            if is_unique:
                unique.append(self.population[i])
                count += 1
            is_unique = True

        return count, float(count)/self.size



def make_terminals(begin, end):
    '''
    Static method to make a list of all possible terminal node values. 
    As an implementation choice, we have chosen half of the terminals 
    to be integral constants, and half to be 'x'

    Parameters:
        begin - The lower bound on the range of constants
        end - The upper bound on the range of constants

    Returns: A list of terminal values
    '''
    terms = []
    at = begin
    while at <= end:
        terms.append(at)
        terms.append('x')
        at += 1
    return terms
