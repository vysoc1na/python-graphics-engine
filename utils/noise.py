import numpy
from noise import pnoise2

def noise(width, height, scale, octaves, persistence, lacunarity, seed):
	height_map = numpy.zeros((height, width))

	for i in range(height):
		for j in range(width):
			x = j / scale
			y = i / scale

			value = pnoise2(
				x + seed,
				y + seed,
				octaves = octaves,
				persistence = persistence,
				lacunarity = lacunarity,
				repeatx = 1024,
				repeaty = 1024,
			)
			height_map[i][j] = value

	return height_map
