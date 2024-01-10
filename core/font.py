import glm
from PIL import Image

class Font():
	def __init__(self):
		self.rows = 6
		self.cols = 9
		self.char_width = 12
		self.char_height = 16

		self.image = Image.open('static/font.png')

		self.data = {
			'A': (0, 0), 'B': (0, 1), 'C': (0, 2), 'D': (0, 3), 'E': (0, 4), 'F': (0, 5), 'G': (0, 6),  'H': (0, 7), 'I': (0, 8),
			'J': (1, 0), 'K': (1, 1), 'L': (1, 2), 'M': (1, 3), 'N': (1, 4), 'O': (1, 5), 'P': (1, 6),  'Q': (1, 7), 'R': (1, 8),
			'S': (2, 0), 'T': (2, 1), 'U': (2, 2), 'V': (2, 3), 'W': (2, 4), 'X': (2, 5), 'Y': (2, 6),  'Z': (2, 7), ' ': (2, 8),
			'1': (3, 0), '2': (3, 1), '3': (3, 2), '4': (3, 3), '5': (3, 4), '6': (3, 5), '7': (3, 6),  '8': (3, 7), '9': (3, 8),
			'!': (4, 0), '?': (4, 1), '(': (4, 2), ')': (4, 3), '[': (4, 4), ']': (4, 5), '/': (4, 6), '\\': (4, 7), '%': (4, 8),
			'.': (5, 0), ',': (5, 1), ';': (5, 2), ':': (5, 3), '*': (5, 4), '-': (5, 5), '+': (5, 6),  '=': (5, 7), '"': (5, 8),
		}

	def translate(self, text):
		# convert text to capitl letters
		text = text.upper()
		# replace zero by "o", they look the same
		text = text.replace('0', 'O')

		text_data = []
		for char in text:
			text_data.append(self.data[char])
		return text_data

	def get_texture(self, text, padding, color):
		text_data = self.translate(text)

		texture_size = (
			int(self.char_width * len(text) + padding.x*2),
			int(self.char_height + padding.y*2),
		)
		texture = Image.new('RGBA', texture_size, (0, 0, 0, 0))

		for i, (row, col) in enumerate(text_data):
			char_start_x = i * self.char_width
			char_start_y = 0

			char_image = self.image.crop((
				col * self.char_width,
				row * self.char_height,
				(col + 1) * self.char_width,
				(row + 1) * self.char_height,
			))

			texture.paste(char_image, (int(char_start_x + padding.x), int(char_start_y + padding.y)))

		texture = texture.transpose(Image.FLIP_TOP_BOTTOM)

		color = (int(color.x * 255), int(color.y * 255), int(color.z * 255), 255)
		solid_color_texture = Image.new("RGBA", texture.size, color)
		mask = texture.split()[3]
		colored_texture = Image.composite(solid_color_texture, texture, mask)

		return colored_texture
