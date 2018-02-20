
patterns = []
slices = []

slices_per_tile = []


def save_slices (slices, filename):
	with open (filename, "w") as fw:
		# Write the header
		fw.write("{}\n".format(len(slices)))

		# Write slices
		for slice in slices:
			fw.write("{} {} {} {}\n".format(slice[0], slice[1], slice[2], slice[3]))


def load_slices (filename):
	slices = []

	with open(filename, "r") as fr:
		# Read header
		num_slices = int(fr.readline().strip())

		# Read slices
		for _ in range(num_slices):
			slice = tuple([int(val) for val in fr.readline().strip().split(" ")])
			slices.append(slice)

	return slices


def create_patterns (min_ingredients, max_size):
	for r in range(1, max_size+1):
		for c in range(1, max_size+1):
			if min_ingredients*2 <= r * c <= max_size:
				patterns.append((r, c))


def create_all_slices (pizza, min_ingredients):
	max_row = len(pizza)
	max_col = len(pizza[0])

	global slices_per_tile
	slices_per_tile = [[[] for _ in range(max_col)] for _ in range(max_row)]
	slice_idx = 0

	# For all the start points in the matrix
	for r_idx in range(max_row):
		for c_idx in range(max_col):
			# For all the possible patterns
			for pattern in patterns:
				try:
					if count_ingredients((r_idx, c_idx), pattern, pizza) >= min_ingredients:
						slice = (r_idx, c_idx, r_idx+pattern[0]-1, c_idx+pattern[1]-1)

						# Save the slice in all the covering tiles
						for i in range(slice[0], slice[2]+1):
							for j in range(slice[1], slice[3]+1):
								slices_per_tile[i][j].append(slice_idx)

						slice_idx += 1

						slices.append(slice)
				except IndexError:
					pass


def compute_per_tile (pizza):
	global slices_per_tile
	slices_per_tile = [[[] for _ in range(len(pizza[0]))] for _ in range(len(pizza))]

	for idx, slice in enumerate(slices):
		for i in range(slice[0], slice[2]+1):
			for j in range(slice[1], slice[3]+1):
				slices_per_tile[i][j].append(idx)


def count_ingredients (coords, pattern, pizza):
	r, c = coords
	dr, dc = pattern

	num_mushroom = 0
	num_tomatoes = 0
	for x in range (r, r+dr):
		for y in range (c, c+dc):
			if pizza[x][y]:
				num_mushroom += 1
			else:
				num_tomatoes += 1

	return min(num_mushroom, num_tomatoes)


def save_to_file ():
	pass


def load_from_file ():
	pass
	

