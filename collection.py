import random

class collection(list):
	'''A list of tuples representing the cards face-up on the table in a game of Set

	Each card is represented with a tuple where each element represents a property of that
	card.  In a normal game of set there are four dimensions (color, shading, shape, and
	count) and a dimensional range of three (three possible values per dimension), so a
	tuple representing cards in a normal game would have four integers, each within the
	range of 0-2
	'''

	def __init__(self, numOfDimensions, dimensionRange, numOfCards):
		'''Generate a random collection of cards

		Args:
			numOfDimensions: The number of properties (color, shape, etc) each card can have
			dimensionRange:  How many variations there are for each property
			numOfCards:      The number of cards in a collection (e.i. on the table face up)

		Works by (effectively) assigning a unique number to each possible card in the deck,
		randomly generating a numOfCards sized list from those numbers, and then converting
		each number to a tuple representing the properties of each card.
		'''

		# Make sure arguments are all integers
		if type(numOfDimensions)!=int or type(dimensionRange)!=int or type(numOfCards)!=int:
			raise ValueError("All arguments to collection constructor must be ints")

		# Determine the maximum deck size, and make sure numOfCards doesn't exceed it
		sizeOfDeck = dimensionRange**numOfDimensions
		if numOfCards > sizeOfDeck:
			raise ValueError("numOfCards exceeds the number of cards in the deck")

		# Store dimension count and range
		self.numOfDimensions = numOfDimensions
		self.dimensionRange = dimensionRange

		# Generate a list of random unique numbers to represent the cards
		cardNumList = random.sample(xrange(sizeOfDeck), numOfCards)

		# Translate each card's number into a card tuple
		for cn in cardNumList:
			newCard = [0]*numOfDimensions
			for d in xrange(numOfDimensions):
				newCard[d] = cn%dimensionRange
				cn/= dimensionRange
			self.append(tuple(newCard))

