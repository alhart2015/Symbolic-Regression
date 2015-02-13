
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
		vals = line.split("\t")
		# print vals
		# I noticed there were 4 columns, i'm not sure which column corresponds
		# to which data point x or y
		x.append(float(vals[0]))
		y.append(float(vals[1]))
		# y.append(int(vals[2]))
		# y.append(int(vals[3]))

	return x, y


def make_test_set(x, y, percent):
    '''
    Splits x and y lists into training and test sets. The resulting training
    sets will use a random subset of the data.

    Parameters:
        x - The list of x-values
        y - The list of y-values
        percent - The percent of the data that will be used to train

    Returns: A 4-tuple (x_train, y_train, x_test, y_test)
    '''
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    for i in xrange(len(x)):
        r = random.random()
        if r < percent:
            x_train.append(x[i])
            y_train.append(y[i])
        else:
            x_test.append(x[i])
            y_test.append(y[i])

    return x_train, y_train, x_test, y_test


#################################################################
""" generate the succeeding generation """

def next_gen(pop, operations, terminals, xData, yData, diversity):
	REPRODUCTION_RATE = .05
	NUM_MUTATIONS = int(math.ceil(.1*len(pop)))
	MUTATION_RATE = .4
	DEPTH_CUTOFF = 16
	top_error = pop[0].error
	current_max_depth = pop[0].max_depth
	total_score = pop_score(pop)

	if diversity < .8:
		NUM_MUTATIONS *= 2

	top_ten_percent = int(math.ceil(len(pop)*REPRODUCTION_RATE))

	new_gen = []

	#Reproduce the best members of the current generation
	for i in range(top_ten_percent):
		# print 'spencer'
		new_gen.append(pop[i])
		# pop[i].to_string()

	#Mutate random individuals in population
	for i in range(NUM_MUTATIONS/2):
		if pop[0].error < 300:
			t = random.choice(pop[top_ten_percent/5:])
		else:
			t = random.choice(pop[5:])
		#t.mutate(t.root, 1, 0, .5, operations, terminals)
		t.mutate2(t.root, MUTATION_RATE, operations, terminals)
		t.calc_error(xData, yData)

	#for i in range(NUM_MUTATIONS/2):
	#	if pop[0].error < 300:
	#		t = random.choice(pop[top_ten_percent/5:])
	#	else:
	#		t = random.choice(pop[5:])
	#	t.subtree_mutate(MUTATION_RATE, t.root, operations, terminals, 5)
	#	t.fix_depth(t.root, 1)
	#	t.calc_error(xData, yData)

	""" Fitness based selection for crossingover """
	
	for i in xrange(top_ten_percent*3):
		p1 = select_individual(pop, total_score)
		p2 = select_individual(pop, total_score)

		while p2 == p1:
			# print 'alden'
			p2 = select_individual(pop, total_score)

		copy1 = deepcopy(pop[p1])
		copy2 = deepcopy(pop[p2])
		copy1.crossover(copy2)
		new_gen.append(copy1)
		# new_gen.append(deepcopy(pop[p1]).crossover(deepcopy(pop[p2])))
	

	""" Tournament selection for crossing over """
	tourny_size = int(math.floor(len(pop)*.3))
	while len(new_gen) < len(pop):
		winners = tournament_selection(tourny_size, pop, 2)
		c1 = deepcopy(winners[0])
		c2 = deepcopy(winners[1])
		c1.crossover(c2)
		c1.calc_error(xData, yData)
		#new_gen.append(c1)
		if c1.max_depth < current_max_depth:
			new_gen.append(c1)
		else:
			if c1.error < top_error and c1.max_depth < DEPTH_CUTOFF:
				new_gen.append(c1)
				current_max_depth = c1.max_depth
			else:
				new_gen.append(init_pop(1, xData, yData)[0])

	return new_gen

def select_individual(pop, total):
	r = random.random()
	at = 0
	acum = 0
	#i = 0
	maxim = len(pop)-1
	while r > (pop[at].score/total) + acum and at < maxim:
		# print i
		#i += 1
		# print "in select_individual:", at, r, acum, pop[at].score/total
		acum += pop[at].score/total
		at += 1

	return at

def pop_score(pop):
	total = 0
	for p in pop:
		total += p.score
	return total

def tournament_selection(size, pop, winners):
	
	selected = random.sample(range(0, len(pop)-1), size)
	tournament_pool = []
	for s in selected:
		tournament_pool.append(pop[s])

	tournament_pool.sort(key=lambda p:p.score, reverse=True)

	return tournament_pool[0:winners]

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

def init_pop(size, xData, yData):
	""" This function generates a list of symbol trees of a user defined
	size to be used as the first generation of genetic programming
	"""
	terminals = make_terminals(-5,5)
	operations = ['+', '-', '*', '/']
	cutoff = .5
	depth_limit = 5
	pop = []
	# print terminals
	# print operations
	# print

	for i in range(size):
		op = operations[random.randint(0,len(operations)-1)]
		n = OpNode(op, 0)
		t = SymbolTree(n)
		add_children(cutoff, depth_limit, 1, terminals, operations, t.root, t)
		t.calc_error(xData, yData)
		pop.append(t)
		# print
	return pop

def add_children(cutoff, depth_limit, at, terminals, operations, node, tree):
	"""
	This recursive function generates a random symbol tree given starting node,
	a percent chance of generating a terminal node, a maximum depth limit,
	and a set of terminal and operator values
	"""
	check_left = random.random()
	check_right = random.random()

	# print "Depth: " + str(at)
	# print "cutoff: " + str(cutoff) + " check left: " + str(check_left) + " check right" + str(check_right)

	if check_left < cutoff or at >= depth_limit:
		r = random.choice(terminals)
		left = OpNode("", r)
		left.depth = at+1
		node.left = left
		tree.size += 1
	else:
		op = random.choice(operations)
		left = OpNode(op, 0)
		node.left = left
		left.depth = at+1
		tree.size += 1
		add_children(cutoff, depth_limit, at+1, terminals, operations, left, tree)

	if check_right < cutoff or at > depth_limit:
		r = random.choice(terminals)
		right = OpNode("", r)
		node.right = right
		right.depth = at+1
		tree.size += 1
	else:
		r = random.choice(operations)
		right = OpNode(r, 0)
		node.right = right
		right.depth = at+1
		tree.size += 1
		add_children(cutoff, depth_limit, at+1, terminals, operations, right, tree)

	if at > tree.max_depth:
		tree.max_depth = at

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
		for p in unique:
			if is_same(pop[i], p):
				is_unique = False
		if is_unique:
			unique.append(pop[i])
		is_unique = True

	return float(len(unique))/len(pop)

def low_score(pop):
	best = 123456
	for p in pop:
		if p.error < best:
			best = p.error
	return best

def test(x_vals, y_vals):
	#x_vals = [1,2,3]
	#y_vals = [2,0,-2]

	terminals = make_terminals(-5, 5)
	operations = ['+', '-', '*', '/']
	gen_size = 500
	num_generations = 25
	pop = init_pop(gen_size, x_vals, y_vals)
	for i in xrange(num_generations):
		pop.sort(key=lambda p: p.error)
		print "    GENERATION:", i
		print "        depth:", pop[0].max_depth
		print "        error:", pop[0].error
		diversity = compare_all(pop)
		print "        diversity:", diversity
		#print "        actual best:", low_score(pop)
		if pop[0].error <=.2:
			break
		pop = next_gen(pop, operations, terminals, x_vals, y_vals, diversity)

		#x = compare_all(pop) 
		#print "diversity by equality:", x
		#print "diversity by score:", count_score(pop)

	return pop[0]

#############################################################
def experiment():
	x_vals, y_vals = getData("G1Data2.txt")
	x_train, y_train, x_test, y_test = make_test_set(x_vals, y_vals, .8)

	evolutions = []
	for i in range(10):
		print "Evolution",i
		winner = test(x_train, y_train)
		winner.to_string()
		print "error:", winner.error, " score:", winner.score
		evolutions.append(winner)

	test_evolve = []
	for e in evolutions:
		c = deepcopy(e)
		c.calc_error(x_test, y_test)
		test_evolve.append(c)
	test_evolve.sort(key=lambda p:p.error)
	print "Best of the GP Winners:"
	test_evolve[0].to_string()
	print "error:", test_evolve[0].error
	

experiment()

