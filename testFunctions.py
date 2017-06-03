from collection import collection
from setSolver import findSets
from timeit import Timer



def findSetsBrute(coll, setSize):
	"""Iterates over every possible group of setSize cards and determines whether they
	form a set or not
	"""

	def helper(partialSet, index, coll, setSize, listOfSets):

		# If the group of cards is big enough, check to see if it's a set
		if len(partialSet)>=setSize:
			simTable = [0]*coll.numOfDimensions
			for card in partialSet:
				for ocard in partialSet:
					for dim in xrange(coll.numOfDimensions):
						simTable[dim]+= card[dim]==ocard[dim]
			for simCount in simTable:
				if simCount!=setSize and simCount!=setSize*setSize:
					return
			listOfSets.append(tuple(partialSet))
			return

		# Stop if out of cards
		if index>=len(coll):
			return

		# Form a partial set with every remaining card
		for cardIndex, card in enumerate(coll[index:], index):
			helper(partialSet+[card], cardIndex+1, coll, setSize, listOfSets)
	

	# Type check
	if type(coll)!=collection:
		raise ValueError("Arg0 should be collection")
	if type(setSize)!=int:
		raise ValueError("Arg1 should be int")

	# Initialize and run helper
	listOfSets = []
	helper([], 0, coll, setSize, listOfSets)
	return listOfSets
			


def findSetsTest(coll, setSize):

	def helper(cardList, index, coll, setSize, listOfSets):
		'''Recursively builds sets and appends them to listOfSets

		"cardList" represents a partial set of cards composed of cards with indices
		less than "index"
		'''

		# Check if current cardList is big enough
		if len(cardList)==setSize:
			listOfSets.append(tuple(cardList))
			return

		# Check if at end of collection
		if index>=len(coll):
			return

		# Number of simalarities per dimension between card and other cards in list
		simTable = [0]*coll.numOfDimensions
		for ocard in cardList:
			for dim in xrange(coll.numOfDimensions):
				simTable[dim] += coll[index][dim]==ocard[dim]

		# For each dimension, this card should be different from all others or the same:
		#  in other words, each element in simTable should be zero or len(cardList)
		addCard = True
		for dim in xrange(coll.numOfDimensions):
			simCount = simTable[dim]
			if simCount!=0 and simCount!=len(cardList):
				addCard = False
				break
			# If different from all other cards, make sure existing cards different from each other
			if simCount==0 and len(cardList)>1:
				if cardList[0][dim]==cardList[1][dim]:
					addCard = False
					break
		if addCard:
			helper(cardList+[coll[index]], index+1, coll, setSize, listOfSets)
		helper(cardList, index+1, coll, setSize, listOfSets)
	

	# Type check
	if type(coll)!=collection:
		raise ValueError("Arg0 should be a collection")
	if type(setSize)!=int:
		raise ValueError("Arg1 should be an integer")
	
	# Initialize and run helper
	setList = []
	helper([], 0, coll, setSize, setList)
	return setList



def benchmark(dims, rang, collectionSize, setSize, functionList):
	'''Takes a list of set-finding functions and benchmarks them with the same collection
	'''
	print "Benchmark:"
	print " %d dimensions," % dims,
	print "%d values per dimension," % rang,
	print "%d cards total," % collectionSize,
	print "%d cards per set." % setSize
	coll = collection(dims, rang, collectionSize)
	setCount = len(findSets(coll, setSize))
	print " Time taken to find", setCount, "sets:"
	for f in functionList:
		fname = f.__name__
		timer = Timer(lambda: f(coll, setSize))
		print " %s%s:  " % (fname, " "*(15-len(fname))),
		print timer.timeit(number=1)
	print ""
	# Source: on how to use Timer:
	#http://stackoverflow.com/questions/7523767/how-to-use-python-timeit-when-passing-variables-to-functions



def consistencyTest(dims, rang, collectionSize, setSize, func1, func2, trials):
	'''Takes two set-finding functions and runs them both multiple times with randomly generated sets, to test if their results are consistent
	'''
	print "Consistency test on functions %s and %s." % (func1.__name__,func2.__name__)
	print " %s trials, " % trials,
	print "%d dimensions," % dims,
	print "%d values per dimension," % rang,
	print "%d cards total," % collectionSize,
	print "%d cards per set:" % setSize
	total = 0
	for _ in xrange(trials):
		coll = collection(dims, rang, collectionSize)
		r1 = func1(coll,setSize)
		r2 = func2(coll,setSize)
		if set(r1)!=set(r2):
			print " FAILURE\n"
			return False
		total+= len(r1)
	print " Average number of sets: %d" % (total/trials)
	print " Pass\n"
	return True


