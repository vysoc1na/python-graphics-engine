import glm
from PIL import Image

class Font():
	def __init__(self):
		self.rows = 8
		self.cols = 16
		self.char_width = 70
		self.char_height = 80

		self.image = Image.open('static/font.png')

		self.data = {
			' ':  (0, 2), '!': (1, 2), '"': (2, 2), '#': (3, 2), '$': (4, 2), '%': (5, 2), '&': (6, 2), '\'': (7, 2), '(': (8, 2), ')': (9, 2), '*': (10, 2), '+': (11, 2), ',':  (12, 2), '-': (13, 2), '.': (14, 2), '/': (15, 2),
			'0':  (0, 3), '1': (1, 3), '2': (2, 3), '3': (3, 3), '4': (4, 3), '5': (5, 3), '6': (6, 3), '7':  (7, 3), '8': (8, 3), '9': (9, 3), ':': (10, 3), ';': (11, 3), '<':  (12, 3), '=': (13, 3), '>': (14, 3), '?': (15, 3),
			'@':  (0, 4), 'A': (1, 4), 'B': (2, 4), 'C': (3, 4), 'D': (4, 4), 'E': (5, 4), 'F': (6, 4), 'G':  (7, 4), 'H': (8, 4), 'I': (9, 4), 'J': (10, 4), 'K': (11, 4), 'L':  (12, 4), 'M': (13, 4), 'N': (14, 4), 'O': (15, 4),
			'P':  (0, 5), 'Q': (1, 5), 'R': (2, 5), 'S': (3, 5), 'T': (4, 5), 'U': (5, 5), 'V': (6, 5), 'W':  (7, 5), 'X': (8, 5), 'Y': (9, 5), 'Z': (10, 5), '[': (11, 5), '\\': (12, 5), ']': (13, 5), '^': (14, 5), '_': (15, 5),
			'\'': (0, 6), 'a': (1, 6), 'b': (2, 6), 'c': (3, 6), 'd': (4, 6), 'e': (5, 6), 'f': (6, 6), 'g':  (7, 6), 'h': (8, 6), 'i': (9, 6), 'j': (10, 6), 'k': (11, 6), 'l':  (12, 6), 'm': (13, 6), 'n': (14, 6), 'o': (15, 6),
			'p':  (0, 7), 'q': (1, 7), 'r': (2, 7), 's': (3, 7), 't': (4, 7), 'u': (5, 7), 'v': (6, 7), 'w':  (7, 7), 'x': (8, 7), 'y': (9, 7), 'z': (10, 7), '{': (11, 7), ':':  (12, 7), '}': (13, 7), '~': (14, 7), ' ': (15, 7),
		}

	def translate(self, text):
		text_data = []
		for char in text:
			text_data.append(self.data[char])
		return text_data

	def get_texture(self, text, padding):
		text_data = self.translate(text)

		texture_size = (
			int(self.char_width * len(text) + padding.x*2),
			int(self.char_height + padding.y*2),
		)
		texture = Image.new('RGBA', texture_size, (0, 0, 0, 0))

		for i, (col, row) in enumerate(text_data):
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

		return texture
