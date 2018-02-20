import slices as slices_functions

class Solution:

	def __init__ (self, pizza, slices=[]):
		self.pizza = pizza
		self.coverage = [[-1 for _ in range(len(self.pizza[0]))] for __ in range(len(self.pizza))]
		self.slices = {}
		self.score = 0

		self.next_slice_idx = 0

		for sl in slices:
			self.add_slice(sl)


	def add_slice (self, slice):
		# Verify the ability to add the slice
		for x in range(slice[0], slice[2]+1):
			for y in range(slice[1], slice[3]+1):
				if self.coverage[x][y] != -1:
					return False

		# Add the slice
		for x in range(slice[0], slice[2]+1):
			for y in range(slice[1], slice[3]+1):
				self.coverage[x][y] = self.next_slice_idx

		# register the slice
		self.slices[self.next_slice_idx] = slice
		self.next_slice_idx += 1

		# modify the score
		self.score += (slice[2]+1-slice[0]) * (slice[3]+1-slice[1])

		return True


	def remove_slice (self, row, col):
		# if no cover
		if self.coverage[row][col] == -1:
			return

		# Get the slice
		idx = self.coverage[row][col]
		slice = self.slices[idx]

		# remove from coverage
		for x in range(slice[0], slice[2]+1):
			for y in range(slice[1], slice[3]+1):
				self.coverage[x][y] = -1

		# remove from solution
		del self.slices[idx]

		# remove from score
		self.score -= (slice[2]+1-slice[0]) * (slice[3]+1-slice[1])

		
	def to_string(self):
		for r_idx, row in enumerate(self.pizza):
			line = "{}\t".format(r_idx)
			for c_idx, val in enumerate(self.pizza[r_idx]):
				if self.coverage[r_idx][c_idx] != -1:
					line += "M" if self.pizza[r_idx][c_idx] else "T"
				else:
					line += "m" if self.pizza[r_idx][c_idx] else "t"
			print(line)


	def save_solution (self, name=""):
		slices_functions.save_slices (list(self.slices.values()), "solutions/{}_{}.txt".format(name, self.score))
		print("{} saved".format(self.score))


	def load_solution (self, filename):
		slices = slices_functions.load_slices(filename)
		for sl in slices:
			self.add_slice(sl)


	def print_solution (self):
		print (len(self.slices))

		for part in self.slices.values():
			print("{} {} {} {}".format(part[0], part[1], part[2], part[3]))

		
