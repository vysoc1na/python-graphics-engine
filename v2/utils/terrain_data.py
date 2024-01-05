import glm

def get_terrain_data(height_map):
	rows, cols = height_map.shape
	result_array = []

	# iterate over 2x2 submatrices and flatten them
	for i in range(rows - 1):
		for j in range(cols - 1):
			submatrix = height_map[i:i + 2, j:j + 2]
			result_array.append({
				'position': glm.vec2(i, j),
				'corners': submatrix.flatten()
			})

	return result_array
