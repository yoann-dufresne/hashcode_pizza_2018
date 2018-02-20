from gurobipy import *

import slices as slices_module
from solution import Solution


def generate_solution (prev_sol, hole=None):
	# Create new solution
	solution = Solution(prev_sol.pizza, prev_sol.slices.values())

	# look for possible slices
	possible_slices = {}
	possible_slices_per_tile = {}
	# enumerate all the tiles
	possible_idxs = []
	if hole == None:
		for i, row in enumerate(prev_sol.coverage):
			for j, val in enumerate(row):
				if val == -1:
					possible_idxs += slices_module.slices_per_tile[i][j]
	else:
		for i in range(hole[0], hole[2]):
			for j in range(hole[1], hole[3]):
				possible_idxs += slices_module.slices_per_tile[i][j]
	# extract uniq idxs
	uniq = set(possible_idxs)
	# Look for possible tiles
	for idx in uniq:
		possible = True
		slice = slices_module.slices[idx]
		for i in range(slice[0], slice[2]+1):
			for j in range(slice[1], slice[3]+1):
				if prev_sol.coverage[i][j] != -1:
					possible = False

		if possible:
			#save slice
			possible_slices[idx] = slice
			# prepare the constraints
			for r in range(slice[0], slice[2]+1):
				# Init row
				if not r in possible_slices_per_tile:
					possible_slices_per_tile[r] = {}
				# fill row
				for c in range(slice[1], slice[3]+1):
					# Init col
					if not c in possible_slices_per_tile[r]:
						possible_slices_per_tile[r][c] = []
					# fill col
					possible_slices_per_tile[r][c].append(idx)

	# If no slice can be put on
	if len(possible_slices) == 0:
		return prev_sol

	# Create MIP model
	m = Model("mip")
	# m.setParam( 'OutputFlag', False )
	vars = {}
	sizes = {}

	# Add all the possible slices to the model
	for idx in possible_slices:
		slice = possible_slices[idx]
		vars[idx] = m.addVar(vtype=GRB.BINARY, name="{}".format(idx))
		sizes[idx] = (slice[2]+1 - slice[0]) * (slice[3]+1 - slice[1])

	# Create the maximization objective
	m.setObjective(quicksum([vars[idx] * sizes[idx] for idx in vars]), GRB.MAXIMIZE)

	# Add one constraint per tile
	constraint_id = 0
	for row_idx in possible_slices_per_tile:
		for col_idx in possible_slices_per_tile[row_idx]:
			sl_list = possible_slices_per_tile[row_idx][col_idx]
			# no slice on the tile
			if len(sl_list) == 0:
				continue

			# add a constraint on the tile
			m.addConstr(quicksum([vars[idx] for idx in sl_list]) <= 1, "c{}".format(constraint_id))
			constraint_id += 1

	m.optimize()

	for v in m.getVars():
		# print(v.varName, v.x)
		if v.x == 1:
			solution.add_slice(possible_slices[int(v.varName)])

	return solution
