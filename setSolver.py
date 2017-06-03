from collection import collection

def findSets(coll, setSize):
	"""Generates a list containing all sets that can be made from the cards in a collection
	
	Args:
		coll:     The collection to be searched for sets
		setSize:  The size of the sets to be searched for


	How it works:

	This function essentially takes the problem of finding "sets" (as defined by the
	rules of the game) and reduces it to a series of searches for fixed sized cliques
	within graphs.  Imagine that every card has been laid out in a line, from left to
	right.  Take the leftmost card, and then divide the remaining cards into groups based
	on the dimensions in which they vary with the leftmost card (e.x. every card with
	the same color and shape but different shading and count to the leftmost card go
	into one pile, while every card with just the same shape as the leftmost card but
	different colors&count&shading go into another pile, while every card that is
	different in every way from the leftmost card goes into yet another pile, etc).
	
	At this point, you can take a pile, and generate a graph from the cards within it,
	where an edge exists between two cards if the relationship between those cards is
	consistent with their relationship with the leftmost card (e.x. if you're going
	through the pile where the colors and shapes are the same with the leftmost card,
	then you can create an edge between two cards if their count and shading are
	different from each other).

	Once your graph is generated, you can now take every clique of size (setSize-1),
	and use it to add a set (composed of the leftmost card and the cards in the clique)
	to the setList.  Note that you don't need to include the leftmost card in the graph:
	since you'd be able to draw an edge between it and every other card, it's a given
	that any clique in the graph will also form a clique with the leftmost card.

	Once you've used this technique on every one of the groups you originally formed,
	you can put each card back into the line you originally formed, discard the leftmost
	card, and then repeat the whole process with the new leftmost card: if you do this
	until you're out of cards, you've found every possible set.

	"""


	def formAndProcessGroups(lcardIndex, lcard, setList):
		"""
		The "lcard" variable is the 'leftmost card' referred to in the description above.
		"diffGroups" is a dictionary used to store each of the groups that have been
		formed via each card's relation to the leftmost card; the values in the dictionary
		are lists of the indices of the cards belonging to the group, while the key is a
		frozenset which represents the relationship between the cards in the group and the
		leftmost card.  For example: if the dimensions are "color","shape", and "count"
		(with enumerations 0,1, and 2 respectively) then every card with the same shape
		as the leftmost card, but with a different colors and count, will belong to the
		group represented with the frozenset (0,2).
		"""

		# Dictionary storing the groups formed in relation to lcard
		diffGroups = {}

		# Iterate over every card to the right of lcard, and add it to the appropriate group
		for rcardIndex,rcard in enumerate(coll[lcardIndex+1:],lcardIndex+1):
			rawDiffKey = set()
			for dim in xrange(coll.numOfDimensions):
				if lcard[dim]!=rcard[dim]:
					rawDiffKey.add(dim)
			diffKey = frozenset(rawDiffKey)
			if diffKey not in diffGroups:
				diffGroups[diffKey] = []
			diffGroups[diffKey]+= [rcardIndex]

		# Find the sets that can be made from the cards in each group (and "lcard")
		for diffKey, group in diffGroups.iteritems():

			# Generate Graph
			edgeSetsList = generateGraph(coll, diffKey, group)

			# Find all cliques in the graph
			cliqueList = []
			for	lowCardGroupIndex, edgeSet in enumerate(edgeSetsList):
				for highCardGroupIndex in edgeSet:
					subClique = (lowCardGroupIndex,highCardGroupIndex)
					findCliques(edgeSetsList, group, setSize, subClique, cliqueList)

			# Convert cliqueList into set of cards
			for clique in cliqueList:
				cardList = [lcard]
				for groupIndex in clique:
					cardList.append(coll[group[groupIndex]])
				setList.append(tuple(cardList))


	def generateGraph(coll, diffKey, group):
		"""
		This functions generates a graph (as described above), and finds all (setSize-1)
		sized cliques within it.  The graph is represented by a list of sets; each card
		in the graph has a set containing pointers to all of the higher group-index cards
		with which that card has edges (if a card has an edge with another card whose
		group-index is lower, the edge is represented in the edgeSet of the other card).

		For example, if you had a graph of three nodes which all had edges between each
		other, edgeSetsList would look like this:
		[set(1,2), set(2), set()]
		"""

		edgeSetsList = [set() for _ in xrange(len(group))]

		for cardGroupIndex, cardIndex in enumerate(group): # cards in set besides "lcard"
			card = coll[cardIndex]
			# Check card against cards in group with higher indices and create edges
			#  where appropriate
			enumeration =  enumerate(group[cardGroupIndex:], cardGroupIndex)
			for hcardGroupIndex, hcardIndex in enumeration:
				hcard = coll[hcardIndex]
				# Check that hcard and card have none of the same values dimensions
				#  where they should be different: if no overlap, create an edge between them
				addEdge = True
				for dim in diffKey:
					if card[dim]==hcard[dim]:
						addEdge = False
						break
				if addEdge:
					edgeSetsList[cardGroupIndex].add(hcardGroupIndex)

		return edgeSetsList


	def findCliques(edgeSetsList, group, setSize, subClique, cliqueList):
		"""
		Takes a clique of size n and finds all super-cliques of size n+1 that can be
		made with the cards in the graph that have a higher groupIndex than the cards
		in the clique.  Then the function is called recursively on the new cliques,
		until all super-cliques of size (setSize-1) have been found. The condition
		that new cards have a higher group-index prevents redundant checks and
		eliminates the possibility of adding duplicate cliques. When a clique of
		size (setSize-1) is discovered, it's appended to the cliqueList.
		"""

		# Check if clique is big enough to be added
		if len(subClique) >= setSize-1:
			cliqueList.append(subClique)
			return

		# Find all n+1 sized cliques
		for hcardGroupIndex in xrange(subClique[-1]+1,len(group)):
			# See if hcard shares edges with cards in clique
			addToClique = True
			for ccardGroupIndex in subClique:
				if hcardGroupIndex not in edgeSetsList[ccardGroupIndex]:
					addToClique = False
					break
			if addToClique:
				newClique = subClique+(hcardGroupIndex,)
				findCliques(edgeSetsList, group, setSize, newClique, cliqueList)


	# Check types for arguments
	if type(coll) != collection:
		raise ValueError("Arg0 should be a collection")
	if type(setSize) != int:
		raise ValueError("Arg1 should be an int")
	
	# Handle fringe setSizes
	if setSize <= 0:
		return []
	if setSize == 1:
		return [(card,) for card in coll]
	if setSize == 2:
		return [(card1,card2) for index,card1 in enumerate(coll) for card2 in coll[index+1:]]

	# The list which is ultimately returned
	setList = []

	# Form and process groups for each card
	for cardIndex,card in enumerate(coll):
		formAndProcessGroups(cardIndex, card, setList)

	return setList

