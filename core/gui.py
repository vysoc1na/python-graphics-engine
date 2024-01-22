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
		font = None,
		size = (160, 80),
		position = (20, 20),
		padding = (0, 0),
		corner = 'TL', # 'TL' | 'TR' | 'BL' | 'BR'
		on_click = debug_on_click,
		text = None,
		color = (1, 1, 1),
		color_hover = (0.9, 0.9, 0.9),
		color_hold = (0.8, 0.8, 0.8),
		text_color = (1, 0, 0),
	):
		self.renderer = renderer
		self.ctx = renderer.ctx
		self.shader_program = renderer.shaders['gui']
		self.window_size = glm.vec2(renderer.window_size)

		self.font = font

		self.padding = glm.vec2(padding)
		if size == 'auto':
			self.size = glm.vec2(6 * len(text), 8) + self.padding
		else:
			self.size = glm.vec2(size) + self.padding
		self.position = glm.vec2(position)
		self.corner = corner
		self.on_click = on_click

		self.text = text
		self.text_color = glm.vec3(text_color)

		self.color = glm.vec3(color)
		self.color_hover = glm.vec3(color_hover)
		self.color_hold = glm.vec3(color_hold)

		self.setup()

		self.init()

	def setup(self):
		print('default setup')

	def init(self):
		self.vertices = self.get_vertices()
		self.texture_coords = self.get_texture_coords()
		self.model = self.get_model()
		if self.text != None:
			self.text_texture = self.get_text_texture()
			self.text_texture.use(1)

		self.vbo = self.renderer.ctx.buffer(numpy.hstack([
			self.vertices,
			self.texture_coords,
		], dtype = 'float32'))

		self.vao = self.renderer.ctx.vertex_array(
			self.shader_program, [
				(self.vbo, '2f 2f', 'in_position', 'in_texture_coords'),
			],
		)

	def handle_on_click(self):
		if self.mouse_in_bound() == True:
			if self.on_click != None:
				self.on_click()

	def get_vertices(self):
		size = self.size / self.window_size

		return numpy.array([
			[-size.x, -size.y],
			[size.x, -size.y],
			[size.x, size.y],
			[-size.x, size.y],
		], dtype = 'float32')

	def get_texture_coords(self):
		return numpy.array([
			[0.0, 0.0],
			[1.0, 0.0],
			[1.0, 1.0],
			[0.0, 1.0],
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

	def get_text_texture(self):
		image = self.font.get_texture(self.text, self.padding, self.text_color)
		texture = self.renderer.ctx.texture(image.size, 4, image.tobytes())
		#texture.build_mipmaps()
		return texture

	# @profile
	def render(self):
		self.text_texture.use(1)
		self.shader_program['model'].write(self.model)

		if self.color == None:
			self.shader_program['in_color'].write(glm.vec3(0, 0, 0))
			self.shader_program['in_color_transparency'].write(glm.float_(0))
		else:
			self.shader_program['in_color_transparency'].write(glm.float_(1))
			if self.mouse_in_bound() == True:
				if pygame.mouse.get_pressed()[0] == True:
					self.shader_program['in_color'].write(self.color_hold)
				else:
					self.shader_program['in_color'].write(self.color_hover)
			else:
				self.shader_program['in_color'].write(self.color)

		if self.text:
			self.shader_program['textured'].value = 1
			self.shader_program['text_texture'].value = 1
		else:
			self.shader_program['textured'].value = 0

		self.vao.render(moderngl.TRIANGLE_FAN)

	def destroy(self):
		# release vbo
		self.vbo.release()
		self.vao.release()
		# release texture
		if self.text != None:
			self.text_texture.release()

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



