#!/usr/bin/env python

from collection import collection
from setSolver import findSets
from testFunctions import *


# Test fringe cases
print "Test with setsize of -1:",findSets(collection(4,3,15),-1)
print "Test with setsize of  0:",findSets(collection(4,3,15), 0)
print "Test with setsize of  1:",findSets(collection(4,3,15), 1)
print "Test with setsize of  2:",findSets(collection(4,3,4), 2)
try:
	findSets("Wrong type", 2)
except ValueError as e:
	print "Invalid type check:", e
try:
	print findSets(collection(4,3,15), "Wrong type")
except ValueError as e:
	print "Invalid type check:", e


# Test findSets and findSetsTest for consistency

# Make sure findSetsTest actually works
assert(consistencyTest(4,   3,  15,  3, findSetsTest, findSetsBrute, 30))
assert(consistencyTest(2,   4,  15,  4, findSetsTest, findSetsBrute, 10))
assert(consistencyTest(2, 100, 100,  2, findSetsTest, findSetsBrute, 5))
assert(consistencyTest(2,1000,  10, 10, findSetsTest, findSetsBrute, 2))

# Test findSets against findSetsBrute
assert(consistencyTest(4,   3,  15,  3, findSets, findSetsBrute, 30))
assert(consistencyTest(2,   4,  15,  4, findSets, findSetsBrute, 10))
assert(consistencyTest(2, 100, 100,  2, findSets, findSetsBrute, 5))
assert(consistencyTest(2,1000,  10, 10, findSets, findSetsBrute, 2))

# More rigorous test of findSets against findSetsTest
assert(consistencyTest(   2, 1000,  15,   3, findSets, findSetsTest, 30))
assert(consistencyTest(   2, 1000,  15,  15, findSets, findSetsTest,  5))
assert(consistencyTest(  30,    2,  15,   4, findSets, findSetsTest,  5))
assert(consistencyTest(   4,  100,  50,   3, findSets, findSetsTest,  5))
assert(consistencyTest(   4,    4,  50,   4, findSets, findSetsTest,  5))


# Benchmarking

# Standard sized set deck
benchmark(4,3,15,3,[findSets, findSetsTest, findSetsBrute])

# Effects of increasing one characteristic of a standard deck
benchmark(10,3,15,3,[findSets, findSetsTest, findSetsBrute])
benchmark(4,10,15,3,[findSets, findSetsTest, findSetsBrute])
benchmark(4,3,40,3,[findSets, findSetsTest, findSetsBrute])
benchmark(4,3,15,5,[findSets, findSetsTest, findSetsBrute]) # Always null

# findSets loses much of it's advantage when the range for each dimension is high,
#  since a high range increases the likelihood of high graph density
benchmark(3, 1000,20,3,[findSets, findSetsTest])
benchmark(3, 1000,20,5,[findSets, findSetsTest])
benchmark(2,   10,50,3,[findSets, findSetsTest])
benchmark(2,   50,50,3,[findSets, findSetsTest])
benchmark(2, 1000,50,3,[findSets, findSetsTest])

# findSets does better as # of cards in the collection increases
benchmark(4,4,50,4,[findSets, findSetsTest])
benchmark(10,3,80,3,[findSets, findSetsTest])
benchmark(10,3,130,3,[findSets, findSetsTest])
# The below benchmark took a while, but they differed by a factor of 100 when it finished
#benchmark(10,4,200,3,[findSets, findSetsTest])


