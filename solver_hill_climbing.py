import solver_gurobi as gurobi
import random
from solution import Solution


def generate_solution (prev_sol, filename="test"):
	prev_sol = Solution(prev_sol.pizza, prev_sol.slices.values())
	uncovered = []

	while True:
		before = prev_sol.score

		# create hole list
		if len(uncovered) == 0:
			for r_idx, row in enumerate(prev_sol.coverage):
				for c_idx, val in enumerate(row):
					if val == -1:
						uncovered.append((r_idx, c_idx))
			random.shuffle(uncovered)

		# Completly covered
		if len(uncovered) == 0:
			return prev_sol

		# already covered
		pos = uncovered.pop()
		if prev_sol.coverage[pos[0]][pos[1]] != -1:
			continue

		# Make a Hole
		hole = make_a_hole (prev_sol, 40, position=pos)
		removed = prev_sol.score

		# Solve the hole in exact
		prev_sol = gurobi.generate_solution(prev_sol, hole=hole)
		after = prev_sol.score

		# Save the solution
		prev_sol.save_solution(filename)
		print(before, removed, after)


def make_a_hole (sol, size, position=None):
	row = col = -1

	if position == None:
		row = random.randint(0, len(sol.pizza)-size)
		col = random.randint(0, len(sol.pizza[0])-size)
	else:
		row = max(0, position[0]-random.randint(0, size))
		row = min(row, len(sol.pizza)-size)

		col = max(0, position[1]-random.randint(0, size))
		col = min(col, len(sol.pizza)-size)

	for i in range(row, row+size):
		for j in range(col, col+size):
			sol.remove_slice(i, j)

	return (row, col, size)
