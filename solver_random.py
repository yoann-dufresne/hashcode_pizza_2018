from copy import deepcopy
from random import shuffle

import slices as slices_module
from solution import Solution


def generate_solution (pizza):
	# Create new solution
	solution = Solution(pizza)
	# copy all the part to create a random order
	slices = deepcopy(slices_module.slices)
	shuffle(slices)

	# Add all the possible slices following the slices order
	for slice in slices:
		solution.add_slice(slice)

	return solution

