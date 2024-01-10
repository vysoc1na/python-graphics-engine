import glm

from core.gui import GuiElement

class Text(GuiElement):
	def setup(self):
		self.padding = glm.vec2(8, 8)
		self.resize()

		self.text_color = glm.vec3(0, 0, 0)

		self.color = None

		self.on_click = None

	def resize(self):
		self.size = glm.vec2(6 * len(self.text), 8) + self.padding

