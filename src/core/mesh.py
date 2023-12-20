import pygame as pg
import numpy as np
import moderngl as mgl
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
		self.update_uniforms({
			'light.position': self.app.light.position,
			'light.Ia': self.app.light.Ia,
			'light.Id': self.app.light.Id,
			'light.Is': self.app.light.Is,
		})
		# Textures
		if self.mesh.texture != None:
			self.mesh.shader_program['u_texture_0'] = 0
			self.mesh.texture.use(location = 0)
		# Model View Projection
		self.update_mvp()

	def update(self):
		self.m_model = self.get_model_matrix()
		self.update_mvp()
		self.update_uniforms({
			'light.position': self.app.light.position,
			'borderSize': self.border_size,
			'borderColor': self.border_color,
			'transparency': self.transparency,
		})

	def update_mvp(self):
		self.update_uniforms({
			'm_model': self.m_model,
			'm_view': self.app.camera.m_view,
			'm_proj': self.app.camera.m_proj,
			'camPos': self.app.camera.position,
		})

	def render(self):
		if self.is_inside_frustum() == False:
			return

		self.update()

		for component in self.mesh.data['components']:
			# Pass colors to shader
			color = self.color or component['color']
			self.update_uniforms({
				'in_color': glm.vec3(color)
			})
			# Render object to screen
			component['vao'].vao.render(self.app.render_mode)

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
		translation_matrix = glm.translate(glm.mat4(1.0), self.position)
		rotation_quaternion = glm.quat(glm.radians(self.rotation))
		rotation_matrix = glm.mat4_cast(rotation_quaternion)
		scale_matrix = glm.scale(glm.mat4(1.0), self.scale)

		m_model = translation_matrix * rotation_matrix * scale_matrix

		return m_model

	def is_inside_frustum(self):
		# Always render tiles
		if self.mesh.name == 'tile':
			return True
		# Compare distance to camera
		camera_distance = glm.length(self.app.camera.position - self.position)
		if camera_distance > self.app.scene.config['size'] / 1.5:
			return False
    	# Calculate the Model-View-Projection matrix
		mvp_matrix = self.app.camera.m_proj * self.app.camera.m_view * self.m_model
		# Set a frustum limit to determine if a point is inside the frustum
		frustum_limit = 1

		# Check each corner of the object's bounding box in clip space
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
			# Transform the corner to clip space using the Model-View-Projection matrix
			clip_space_corner = mvp_matrix * corner
			clip_space_corner.w += 0.001 # division by zero
			# Check if the transformed coordinates are within the frustum limits
			if -frustum_limit <= clip_space_corner.x / clip_space_corner.w <= frustum_limit:
				if -frustum_limit <= clip_space_corner.y / clip_space_corner.w <= frustum_limit:
					if -frustum_limit <= clip_space_corner.z / clip_space_corner.w <= frustum_limit:
						return True

		return False

	def update_uniforms(self, uniform_dict):
		for name, value in uniform_dict.items():
			self.mesh.shader_program[name].write(value)
