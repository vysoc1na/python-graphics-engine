# from memory_profiler import profile
import numpy
import glm
import moderngl
import pygame

def debug_on_click():
	print('click')

class GuiElement():
	def __init__(
		self,
		renderer,
		size = glm.vec2(80, 40),
		position = glm.vec2(20, 20),
		corner = 'TL', # 'TL' | 'TR' | 'BL' | 'BR'
		on_click = debug_on_click,
	):
		self.renderer = renderer
		self.ctx = renderer.ctx
		self.shader_program = renderer.shaders['gui']
		self.window_size = glm.vec2(renderer.window_size)

		self.size = size
		self.position = position
		self.corner = corner
		self.on_click = on_click

		self.on_init()

	def on_init(self):
		self.color = glm.vec3(1, 0, 0)
		self.hover_color = glm.vec3(0, 0, 1)
		self.hold_color = glm.vec3(1, 0, 1)

		self.vertices = self.get_vertices()
		self.model = self.get_model()

		self.vbo = self.renderer.ctx.buffer(self.vertices)
		self.vao = self.renderer.ctx.vertex_array(
			self.shader_program, [
				(self.vbo, '2f', 'in_position'),
			],
		)

	def handle_on_click(self):
		if self.mouse_in_bound() == True:
			self.on_click()

	def get_vertices(self):
		size = self.size / self.window_size

		return numpy.array([
			-size.x, -size.y,
			size.x, -size.y,
			size.x, size.y,
			-size.x, size.y,
		], dtype = 'float32')

	def get_model(self):
		size = self.size / self.window_size
		position = self.position / self.window_size * 2

		if self.corner == 'TL':
			x = -1 + size.x + position.x
			y = 1 - size.y - position.y
		if self.corner == 'TR':
			x = 1 - size.x - position.x
			y = 1 - size.y - position.y
		if self.corner == 'BL':
			x = -1 + size.x + position.x
			y = -1 + size.y + position.y
		if self.corner == 'BR':
			x = 1 - size.x - position.x
			y = -1 + size.y + position.y

		return glm.translate(glm.mat4(1.0), (x, y, 0))

	# @profile
	def render(self):
		self.shader_program['model'].write(self.model)

		if self.mouse_in_bound() == True:
			if pygame.mouse.get_pressed()[0] == True:
				self.shader_program['in_color'].write(self.hold_color)
			else:
				self.shader_program['in_color'].write(self.hover_color)
		else:
			self.shader_program['in_color'].write(self.color)

		self.vao.render(moderngl.TRIANGLE_FAN)

	def destroy(self):
		self.vbo.release()
		self.vao.release()

	def mouse_in_bound(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()

		width, height = self.window_size
		x, y = self.position
		size = self.size

		if self.corner == 'TL':
			if mouse_x > x and mouse_x < x + size.x:
				if mouse_y > y and mouse_y < y + size.y:
					return True
		if self.corner == 'TR':
			if mouse_x > width - size.x - x and mouse_x < width - x:
				if mouse_y > y and mouse_y < y + size.y:
					return True
		if self.corner == 'BL':
			if mouse_x > x and mouse_x < x + size.x:
				if mouse_y > height - size.y - y and mouse_y < height - y:
					return True
		if self.corner == 'BR':
			if mouse_x > width - size.x - x and mouse_x < width - x:
				if mouse_y > height - size.y - y and mouse_y < height - y:
					return True

		return False

class Gui():
	def __init__(self, renderer):
		self.renderer = renderer
		self.ctx = renderer.ctx
		self.shader_program = renderer.shaders['gui']

		self.poosition = glm.vec2(10, 10)
		self.size = glm.vec2(160, 80)
		self.color = glm.vec3(1, 0, 0)

		self.children = []

	def render(self):
		for item in self.children:
			item.render()

	def destroy(self):
		for item in self.children:
			item.destroy()



