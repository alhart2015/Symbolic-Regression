
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

#####################################################################
""" functions that evaluate trees """

def evaluate_function(x, tree):
	""" This method evaluates the SymbolTree function for every
	x value in the original data selection

	Returns an array of y values 
	"""
	y = []
	for val in x:
		y.append(tree.eval(val))

	return y

def square_error_selection(yData, yTree, tree):
	""" This method generates a selection score based on the square 
	difference between y values at each x value.

	Returns: a selection score for the evaluate_function
	"""
	# one obvious potential downfall of this method is curves that are 
	# above the actual data at some points and below the actual data at
	# other points can end up with a score of 0 just like a curve that matches
	score = 0
	for i in range(len(yData)):
		score += pow(yData[i] - yTree[i], 2)
	tree.score = score
	return score

#################################################################
""" generate the succeeding generation """

def next_gen(pop, total, operations, terminals):
	REPRODUCTION_RATE = .1
	MUTATION_RATE = .1

	new_gen = []

	for i in range(int(math.floor(len(pop)*REPRODUCTION_RATE))):
		new_gen.append(pop[i])

	for i in range(int(math.floor(len(pop)*MUTATION_RATE))):
		m = len(pop)*random.random()
		pop[m].mutate(pop[m].root, 1, 0, .5, operations, terminals)

	while len(new_gen) < len(pop):
		p1 = select_individual(pop, total)
		p2 = select_individual(pop, total)

		while p2 == p1:
			p2 = select_individual(pop, total)

		new_gen.append(pop[p1].crossover(pop[p2]))

	return new_gen
		 

def select_individual(pop, total):
	r = random.random()
	at = 0
	acum = 0
	while (r < ((total-(pop[at].score+acum))/total)) and at < len(pop)-1:
		at += 1
		acum += (total-(pop[at].score+acum))/total
	return at

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

	xData = [1, 2, 3]
	yData = [2, 0, -2]
	gen_size = 3

	pop = init_pop(gen_size)
	total = 0

	print "gen 0"
	for p in pop:
		#p.to_string()
		total += square_error_selection(yData, evaluate_function(xData, p), p)
		print p.score
	print total
	pop.sort(key=lambda p: p.score)
	pop = next_gen(pop, total, operations, terminals)

	print 
	print "gen 1"
	for p in pop:
		p.to_string()



		




main()