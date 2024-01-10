import glm

class List():
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
		index = 0
		for element in self.elements:
			element.position = glm.vec2(
				element.position.x,
				index * (height + self.spacing) + element.position.y,
			)
			element.on_init()

			index += 1

	def handle_on_click(self):
		for element in self.elements:
			element.handle_on_click()

	def render(self):
		for element in self.elements:
			element.render()

	def destroy(self):
		for element in self.elements:
			element.destroy()
