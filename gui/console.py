import glm
import datetime

from gui.text import Text

class Console():
	def __init__(self, renderer, font):
		self.renderer = renderer
		self.font = font

		self.corner = 'BL'
		self.elements_treshold = 8
		self.elements = []

		self.add('console init')

	def add(self, text):
		current_time = datetime.datetime.now().time()
		prefix = f'{current_time.strftime("%H:%M:%S:%f")[:-3]}'
		element = Text(self.renderer, self.font, text = f'[{prefix}] {text}', corner = self.corner)
		element.position = glm.vec2(element.position.x, (len(self.elements) + 1) * element.size.y)
		element.init()

		self.elements.append(element)

		if len(self.elements) > self.elements_treshold:
			element_to_remove = self.elements.pop(0)
			element_to_remove.destroy()
			del element_to_remove

			index = 1
			for element in self.elements:
				element.position = glm.vec2(element.position.x, index * element.size.y)
				element.init()
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
