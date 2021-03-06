
import string
import math
from symbol_tree import SymbolTree
import random
from op_node import OpNode
from copy import deepcopy

def getData(filename):
	""" Retrives data from a text filename

	Returns the data parallel arrays
	"""
	x = []
	y = []
	
	infile = open(filename, "r")
	data = infile.readlines()
	infile.close()
	for line in data:
		vals = line.split(" ")
		# print vals
		# I noticed there were 4 columns, i'm not sure which column corresponds
		# to which data point x or y
		x.append(float(vals[0]))
		y.append(float(vals[1]))
		# y.append(int(vals[2]))
		# y.append(int(vals[3]))

	return x, y

#####################################################################
""" functions that evaluate trees """

def evaluate_function(x, tree):
	""" This method evaluates the SymbolTree function for every
	x value in the original data selection

	Returns an array of y values 
	"""
	y = []
	# print tree
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
	error = 0
	for i in range(len(yData)):
		# error += pow(yData[i] - yTree[i], 2)
		error += abs(float(yData[i]) - yTree[i])
	tree.error = error
	return error

def total_error(population, x_data, y_data):
	'''Calculates the mean squared error of every tree in the population

	Returns: the sum of all errors
	'''
	i = 0
	total = 0
	for t in population:
		total += square_error_selection(y_data, evaluate_function(x_data, t), t)
	return total

def all_scores(error_sum, population):
	'''Calculates the score based on the squared error of each tree

	Returns: the new sum of all the scores
	'''
	new_sum = 0

	for t in population:
		t.score = 1./(1.+t.error)#float(error_sum - t.error)
		new_sum += t.score

	return new_sum


#################################################################
""" generate the succeeding generation """

def next_gen(pop, total, operations, terminals):
	REPRODUCTION_RATE = .1
	MUTATION_RATE = .1

	new_gen = []

	for i in range(int(math.ceil(len(pop)*REPRODUCTION_RATE))):
		# print 'spencer'
		new_gen.append(pop[i])
		# pop[i].to_string()

	for i in range(int(math.ceil(len(pop)*MUTATION_RATE))):
		t = random.choice(pop)
		#t.mutate(t.root, 1, 0, .5, operations, terminals)
		t.mutate2(t.root, .25, operations, terminals)

	while len(new_gen) < len(pop):
		p1 = select_individual(pop, total)
		p2 = select_individual(pop, total)

		while p2 == p1:
			# print 'alden'
			p2 = select_individual(pop, total)

		copy1 = deepcopy(pop[p1])
		copy2 = deepcopy(pop[p2])
		copy1.crossover(copy2)
		new_gen.append(copy1)
		# new_gen.append(deepcopy(pop[p1]).crossover(deepcopy(pop[p2])))

	return new_gen

def select_individual(pop, total):
	r = random.random()
	at = -1
	acum = 0
	i = 0
	while r > (pop[at].score/total) + acum:
		# print i
		# i += 1
		# print "in select_individual:", at, r, acum, pop[at].score/total
		acum += pop[at].score/total
		at -= 1

		
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
		t.append('x')
	return t

def init_pop(size):
	""" This function generates a list of symbol trees of a user defined
	size to be used as the first generation of genetic programming
	"""
	terminals = make_terminals(-5,5)
	operations = ['+', '-', '*', '/']
	cutoff = .5
	depth_limit = 1
	pop = []
	# print terminals
	# print operations
	# print

	for i in range(size):
		op = operations[random.randint(0,len(operations)-1)]
		n = OpNode(op, 0)
		t = SymbolTree(n)
		add_children(cutoff, depth_limit, 1, terminals, operations, t.root)
		pop.append(t)
		# print

	return pop

def add_children(cutoff, depth_limit, at, terminals, operations, node):
	"""
	This recursive function generates a random symbol tree given starting node,
	a percent chance of generating a terminal node, a maximum depth limit,
	and a set of terminal and operator values
	"""
	check_left = random.random()
	check_right = random.random()

	# print "Depth: " + str(at)
	# print "cutoff: " + str(cutoff) + " check left: " + str(check_left) + " check right" + str(check_right)

	if check_left < cutoff or at > depth_limit:
		r = random.randint(0, len(terminals)-1)
		left = OpNode("", terminals[r])
		left.depth = at+1
		node.left = left
	else:
		if node.operator == "^":
			op = random.choice(operations)
			while op == "^":
				op = random.choice(operations)
			left = OpNode(op, 0)
		else:
			r = random.randint(0, len(operations)-1)
			left = OpNode(operations[r], 0)
		node.left = left
		left.depth = at+1
		add_children(cutoff, depth_limit, at+1, terminals, operations, left)

	if check_right < cutoff or at > depth_limit or node.operator == "^":
		if node.operator == "^":
			term = random.choice(terminals)
			while term == "x":
				term = random.choice(terminals)
			right = OpNode("", term)
		else:
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

def count_score(pop):
	scores = []
	for p in pop:
		if p.score not in scores:
			scores.append(p.score)
	return float(len(scores))/len(pop)

def is_same(tree1, tree2):
	return same_help(tree1.root, tree2.root)

def same_help(n1, n2):
	if n1 and n2 and n1.operator == n2.operator and n1.value == n2.value:
		if not n1.left and not n1.right and not n2.left and not n2.right:
			return True
		else:
			return same_help(n1.left, n2.left) and same_help(n1.right, n2.right)
	return False

def compare_all(pop):
	comp = []
	unique = []
	is_unique = True
	count = 0
	for i in range(len(pop)):
		print "Starting comparisons for:"
		pop[i].to_string()
		print "Compares:"
		for p in unique:
			p.to_string()
			if is_same(pop[i], p):
				print "                                      same"
				is_unique = False
			print is_unique
		comp.append(pop[i])
		if is_unique:
			unique.append(pop[i])
		is_unique = True
		print
		print

	print "count:", len(unique)

	return float(len(unique))/len(pop)

def test():
	x_vals, y_vals = getData("test_data.txt")
	#x_vals = [1,2,3]
	#y_vals = [2,0,-2]

	terminals = make_terminals(-10, 10)
	operations = ['+', '-', '*', '/']
	gen_size = 20
	num_generations = 1
	population = init_pop(gen_size)
	for i in xrange(num_generations):
		print "GENERATION:", i
		#print "population:"
		# for t in population:
		# 	t.to_string()
		# 	# print t.error, t.score, t.eval(1), t.eval(2), t.eval(3)
		# 	# print
		error_sum = total_error(population, x_vals, y_vals)
		sum_scores = all_scores(error_sum, population)
		population.sort(key=lambda x: x.score)
		print count_score(population)
		if population[-1].error <=.2:
			break
		population = next_gen(population, sum_scores, operations, terminals)

		x = compare_all(population) 
		print "diversity by equality:", x
		print "diversity by score:", count_score(population)

	print "We found a winner!"
	population[-1].to_string()
	print "error:", population[-1].error, " score:", population[-1].score

"""
	population.sort(key=lambda x: x.score)
	population[-1].to_string()
	print "error:", population[-1].error, " score:", population[-1].score
	print population[-1].eval(1), population[-1].eval(2), population[-1].eval(3)
	population[0].to_string()
	print "error:", population[0].error, " score:", population[0].score
"""
	# terminals = make_terminals(-3, 3)
	# operations = ['+', '-', '*', '/', '^']
	# x_data = [1, 2, 3]
	# y_data = [2, 0, -2]
	# gen_size = 3
	# num_generations = 3
	# population = init_pop(gen_size)
	# for i in xrange(num_generations):
	# 	print "GENERATION:", i
	# 	error_sum = total_error(population, x_data, y_data)
	# 	sum_scores = all_scores(error_sum, population)
	# 	print "population:"
	# 	for t in population:
	# 		t.to_string()
	# 		print t.error, t.score, t.eval(1), t.eval(2), t.eval(3)
	# 		print
	# 	population = next_gen(population, sum_scores, operations, terminals)



#############################################################
test()

