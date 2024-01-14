import glm

class ButtonList():
	def __init__(
		self,
		renderer,
		elements = [],
		spacing = 4,
	):
		self.renderer = renderer
		self.elements = elements
		self.spacing = spacing

		self.on_init()

	def on_init(self):
		height = self.elements[0].size.y
		corner = self.elements[0].corner

		if corner == 'TL' or corner == 'TR':
			index = 0
		if corner == 'BL' or corner == 'BR':
			index = len(self.elements) - 1

		for element in self.elements:
			element.position = glm.vec2(
				element.position.x,
				index * (height + self.spacing) + element.position.y,
			)
			element.on_init()

			if corner == 'TL' or corner == 'TR':
				index += 1
			if corner == 'BL' or corner == 'BR':
				index -= 1

	def handle_on_click(self):
		for element in self.elements:
			element.handle_on_click()

	def render(self):
		for element in self.elements:
			element.render()

	def destroy(self):
		for element in self.elements:
			element.destroy()
