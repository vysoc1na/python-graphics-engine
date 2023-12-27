import glm
import numpy

class Mesh():
	def __init__(
		self,
		geometry,
		material,
		shader_program,
		update_method = None,
	):
		# setup geometry, materials and update methods
		self.geometry = geometry
		self.material = material
		self.update_method = update_method
		# setup shader, vbo, vao
		self.shader_program = shader_program
		# setup combined vertex_data
		self.setup_vertex_data()

	def setup_vertex_data(self):
		# geometry
		vertices = self.geometry.vertices
		normals = self.geometry.normals
		# material
		color = self.material.color
		colors = numpy.full_like(vertices, color, dtype = 'float32')
		# vertex data
		self.vertex_data = numpy.hstack([vertices, normals, colors], dtype = 'float32')

	def get_model_matrix(self):
		translation_matrix = glm.translate(glm.mat4(1.0), self.geometry.position)
		rotation_quaternion = glm.quat(glm.radians(self.geometry.rotation))
		rotation_matrix = glm.mat4_cast(rotation_quaternion)
		scale_matrix = glm.scale(glm.mat4(1.0), self.geometry.scale)
		# model matrix
		model = translation_matrix * rotation_matrix * scale_matrix

		return model

	def render(self, projection, view, model, ctx, render_mode):
		# update callback
		if callable(self.update_method):
			self.update_method(self.geometry, self.material)

		# mvp
		self.shader_program['projection'].write(projection)
		self.shader_program['view'].write(view)
		self.shader_program['model'].write(self.get_model_matrix())
		# vbo
		self.vbo = ctx.buffer(self.vertex_data)
		# vao
		self.vao = ctx.vertex_array(
			self.shader_program, [
				(self.vbo, '3f 3f 3f', 'in_position', 'in_normal', 'in_color'),
			]
		)
		# Render the mesh
		self.vao.render(render_mode)

	def destroy(self):
		self.vao.release()
