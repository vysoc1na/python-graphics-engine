from gui.text import Text

class Console():
	def __init__(self, renderer, font):
		self.renderer = renderer
		self.font = font

		self.elements = []

		self.elements.append(
			Text(renderer, font, text = '[console] TODO', corner = 'BL')
		)

	def handle_on_click(self):
		for element in self.elements:
			element.handle_on_click()

	def render(self):
		for element in self.elements:
			element.render()

	def destroy(self):
		for element in self.elements:
			element.destroy()
