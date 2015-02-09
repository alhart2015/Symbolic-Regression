
import string
import math
from symbol_tree import SymbolTree
import random
from op_node import OpNode

def getData(filename):
	""" Retrives data from a text filename

	Returns the data parallel arrays
	"""
	x = []
	y = []
	
	infile = open(filename, "r")
	data = infile.readlines()

	for line in data:
		vals = line.split(" ")
		# I noticed there were 4 columns, i'm not sure which column corresponds
		# to which data point x or y
		x.append(int(vals[0]))
		x.append(int(vals[1]))
		y.append(int(vals[2]))
		y.append(int(vals[3]))

	return x, y


def evaluate_function(x, tree):
	""" This method evaluates the SymbolTree function for every
	x value in the original data selection

	Returns an array of y values 
	"""
	y = []
	for val in x:
		y.append(tree.eval(val))

	return y

def y_difference_selection(yData, yTree):
	""" This method generates a selection score based on the difference between
	y values at each x value.

	Returns: a selection score for the evaluate_function
	"""
	# one obvious potential downfall of this method is curves that are 
	# above the actual data at some points and below the actual data at
	# other points can end up with a score of 0 just like a curve that matches
	score = 0
	for i in range(len(yData)):
		score += yData[i] - yTree[i]

	return score

#################################################################
	"""
	This section of the code provides functions that create the 
	initial population of individuals
	"""

def make_terminals(begin, end):
	""" This function makes a list of all possible terminals
		node values, where the user can determine the range of 
		values from which the program will chose.

		Returns a list of terminal values
	"""

	t = ['x']
	at = begin
	while (at <= end):
		t.append(at)
		at += 1
	return t

def init_pop(size):
	""" This function generates a list of symbol trees of a user defined
	size to be used as the first generation of genetic programming
	"""
	terminals = make_terminals(-3,3)
	operations = ['+', '-', '*', '/']
	cutoff = .5
	depth_limit = 2
	pop = []
	print terminals
	print operations
	print

	for i in range(size):
		op = operations[random.randint(0,len(operations)-1)]
		n = OpNode(op, 0)
		t = SymbolTree(n)
		add_children(cutoff, depth_limit, 1, terminals, operations, t.root)
		pop.append(t)
		print

	return pop

def add_children(cutoff, depth_limit, at, terminals, operations, node):
	"""
	This recursive function generates a random symbol tree given starting node,
	a percent chance of generating a terminal node, a maximum depth limit,
	and a set of terminal and operator values
	"""
	check_left = random.random()
	check_right = random.random()

	print "Depth: " + str(at)
	print "cutoff: " + str(cutoff) + " check left: " + str(check_left) + " check right" + str(check_right)

	if check_left < cutoff or at > depth_limit:
		r = random.randint(0, len(terminals)-1)
		left = OpNode("", terminals[r])
		left.depth = at+1
		node.left = left
	else:
		r = random.randint(0, len(operations)-1)
		left = OpNode(operations[r], 0)
		node.left = left
		left.depth = at+1
		add_children(cutoff, depth_limit, at+1, terminals, operations, left)

	if check_right < cutoff or at > depth_limit:
		r = random.randint(0, len(terminals)-1)
		right = OpNode("", terminals[r])
		node.right = right
		right.depth = at+1
	else:
		r = random.randint(0, len(operations)-1)
		right = OpNode(operations[r], 0)
		node.right = right
		right.depth = at+1
		add_children(cutoff, depth_limit, at+1, terminals, operations, right)


#############################################################
"""
The main function is for testing purposes only
"""
def main():
	""" Controls the flow of the selection process
	"""
	terminals = make_terminals(-3,3)
	operations = ['+', '-', '*', '/']
	#xPts, yPts = getData("test.txt")
	test = init_pop(2)
	print "parent 1"
	test[0].to_string()
	print test[0].eval(2)
	print "parent 2"
	test[1].to_string()
	print test[1].eval(2)
	test[0].crossover(test[1])
	print "cross 1"
	test[0].to_string()
	print test[0].eval(2)
	print "cross 2"
	test[1].to_string()
	print test[1].eval(2)


main()