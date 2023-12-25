from PIL import Image

def image_to_coordinates(image_path):
	# Open the image
	image = Image.open(image_path)
	image = image.transpose(Image.FLIP_TOP_BOTTOM)

	# Get the size of the image
	width, height = image.size

	# Define the size of each pixel block
	block_size = 10

	# Create an empty list to store coordinates
	coordinates = []

	# Iterate through each block (not each pixel)
	for x_block in range(0, width, block_size):
		for y_block in range(0, height, block_size):
			# Check if any pixel in the block is black
			black_pixel_in_block = any(
				image.getpixel((x, y)) == (0, 0, 0, 255)
				for x in range(x_block, x_block + block_size)
				for y in range(y_block, y_block + block_size)
			)

			# If there is a black pixel in the block, append its coordinates
			if black_pixel_in_block:
				coordinates.append([x_block / block_size, y_block / block_size - 1])

	return coordinates

# Example usage
image_path = "maze.png"
black_pixel_coordinates = image_to_coordinates(image_path)

# Print the coordinates of black pixels
print(black_pixel_coordinates)
