import glm

from core.gui import GuiElement

class Button(GuiElement):
	def setup(self):
		self.padding = glm.vec2(8, 8)
		self.size = glm.vec2(6 * len(self.text), 8) + self.padding

		self.text_color = glm.vec3(1, 1, 1)

		self.color = glm.vec3(0.2, 0.2, 0.2)
		self.color_hover = glm.vec3(0.8, 0, 0)
		self.color_hold = glm.vec3(0, 0, 0.8)

