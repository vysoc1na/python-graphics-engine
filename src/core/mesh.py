import pygame as pg
import numpy as np
import glm
import json

from src.core.vao import Vao

class MeshComponent():
	def __init__(self, app, shader_program, name = 'tile', parent = None, texture_path = None):
		self.app = app
		self.ctx = app.ctx
		self.name = name
		self.shader_program = shader_program
		self.parent = parent

		if texture_path != None:
			self.texture = self.get_texture(texture_path)
		else:
			self.texture = None

		self.data = self.get_data(name)

		self.on_init()

	def on_init(self):
		for component in self.data['components']:
			component['color'] = glm.vec3(component['color'])
			component['vertex_data'] = np.array(component['vertex_data'], dtype = 'f4')

			component['vao'] = Vao(
				self.app,
				shader_program = self.shader_program,
				vertex_data = component['vertex_data'],
			)

	def get_data(self, name):
		with open(f'models/{name}.json', 'r') as f:
			data = json.load(f)
		return data

	def get_texture(self, texture_path):
		texture = pg.image.load(texture_path).convert()
		texture = pg.transform.flip(texture, flip_x = False, flip_y = True)
		texture = self.ctx.texture(size = texture.get_size(), components = 3, data = pg.image.tostring(texture, 'RGB'))
		# mipmaps
		texture.build_mipmaps()

		return texture


class Mesh():
	def __init__(
		self,
		app,
		mesh_component,
		name = 'tile',
		position = (0, 0, 0),
		rotation = (0, 0, 0),
		scale = (1, 1, 1),
		borderSize = 0,
		borderColor = (0, 0, 0),
		transparency = 1,
		color = None,
	):
		self.app = app
		self.ctx = app.ctx

		self.name = name
		self.mesh = mesh_component
		self.color = color

		self.set_position(position)
		self.set_rotation(rotation)
		self.set_scale(scale)
		self.m_model = self.get_model_matrix()

		self.set_border_size(borderSize)
		self.set_border_color(borderColor)

		self.set_transparency(transparency)

		self.on_init()

	def on_init(self):
		# lights
		self.mesh.shader_program['light.position'].write(self.app.light.position)
		self.mesh.shader_program['light.Ia'].write(self.app.light.Ia)
		self.mesh.shader_program['light.Id'].write(self.app.light.Id)
		self.mesh.shader_program['light.Is'].write(self.app.light.Is)
		# textures
		if self.mesh.texture != None:
			self.mesh.shader_program['u_texture_0'] = 0
			self.mesh.texture.use(location = 0)
		# MVP + camera position
		self.update_mvp()

	def update(self):
		self.m_model = self.get_model_matrix()
		# MVP + camera position
		self.update_mvp()
		# lights
		self.mesh.shader_program['light.position'].write(self.app.light.position)
		# borders
		self.mesh.shader_program['borderSize'].write(self.border_size)
		self.mesh.shader_program['borderColor'].write(self.border_color)
		# transparency
		self.mesh.shader_program['transparency'].write(self.transparency)

	def update_mvp(self):
		self.mesh.shader_program['m_model'].write(self.m_model)
		self.mesh.shader_program['m_view'].write(self.app.camera.m_view)
		self.mesh.shader_program['m_proj'].write(self.app.camera.m_proj)
		# camera position (for light calculations)
		self.mesh.shader_program['camPos'].write(self.app.camera.position)

	def render(self):
		self.update()

		for component in self.mesh.data['components']:
			# colors
			if self.color == None:
				self.mesh.shader_program['in_color'].write(component['color'])
			else:
				self.mesh.shader_program['in_color'].write(glm.vec3(self.color))
			# render models only when is on screen
			if self.is_inside_frustum():
				component['vao'].vao.render()

	def destroy(self):
		for component in self.mesh.data['components']:
			component['vao'].vao.release()

	def set_position(self, position):
		self.position = glm.vec3(position)

	def set_rotation(self, rotation):
		self.rotation = glm.vec3(rotation)

	def set_scale(self, scale):
		self.scale = glm.vec3(scale)

	def set_border_size(self, size):
		self.border_size = glm.float_(size)

	def set_border_color(self, color):
		self.border_color = glm.vec3(color)

	def set_transparency(self, transparency):
		self.transparency = glm.float_(transparency)

	def get_model_matrix(self):
		m_model = glm.mat4()
		# translation
		m_model = glm.translate(m_model, self.position)
		# rotation
		m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
		m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
		m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))
		# scale
		m_model = glm.scale(m_model, self.scale)

		return m_model

	def is_inside_frustum(self):
		mvp_matrix = self.app.camera.m_proj * self.app.camera.m_view * self.m_model
		frustum_limit = 4

		for corner in [
			glm.vec4(-1, -1, -1, 1),
			glm.vec4(-1, -1, 1, 1),
			glm.vec4(-1, 1, -1, 1),
			glm.vec4(-1, 1, 1, 1),
			glm.vec4(1, -1, -1, 1),
			glm.vec4(1, -1, 1, 1),
			glm.vec4(1, 1, -1, 1),
			glm.vec4(1, 1, 1, 1)
		]:
			clip_space_corner = mvp_matrix * corner
			if -frustum_limit <= clip_space_corner.x / clip_space_corner.w <= frustum_limit:
				if -frustum_limit <= clip_space_corner.y / clip_space_corner.w <= frustum_limit:
					if -frustum_limit <= clip_space_corner.z / clip_space_corner.w <= frustum_limit:
						return True

		return False
