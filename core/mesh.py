# from memory_profiler import profile
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
		self.should_update = True
		self.shader_program = shader_program

	def setup_vertex_data(self):
		# material colors
		if type(self.material).__name__ == 'TerrainMaterial':
			colors = (1 - self.geometry.colors) * self.material.color_low + self.geometry.colors * self.material.color_high
		else:
			colors = numpy.full_like(self.geometry.vertices, self.material.color, dtype = 'float32')

		# vertex data
		self.vertex_data = numpy.hstack([
			self.geometry.vertices,
			self.geometry.normals,
			self.geometry.texture_coords,
			colors,
		], dtype = 'float32')

	def get_model_matrix(self):
		translation_matrix = glm.translate(glm.mat4(1.0), self.geometry.position)
		rotation_quaternion = glm.quat(glm.radians(self.geometry.rotation))
		rotation_matrix = glm.mat4_cast(rotation_quaternion)
		scale_matrix = glm.scale(glm.mat4(1.0), self.geometry.scale)
		# model matrix
		model = translation_matrix * rotation_matrix * scale_matrix

		return model

	# @profile
	def render(self, projection, view, ctx, render_mode):
		# update callback
		if isinstance(self.update_method, list):
			for update_method in self.update_method:
				if callable(update_method):
					update_method(self.geometry, self.material)
		elif callable(self.update_method):
			self.update_method(self.geometry, self.material)

		# get combined vertex data
		self.setup_vertex_data()
		# update vertices
		self.update(ctx)
		# mvp
		self.shader_program['projection'].write(projection)
		self.shader_program['view'].write(view)
		self.shader_program['model'].write(self.get_model_matrix())
		# render
		self.vao.render(render_mode)

	def update(self, ctx):
		if self.should_update == True:
			# clear previous buffers
			if hasattr(self, 'vbo') and hasattr(self, 'vao'):
				self.destroy()
			# vbo
			self.vbo = ctx.buffer(self.vertex_data)
			# vao
			self.vao = ctx.vertex_array(
				self.shader_program, [
					(self.vbo, '3f 3f 2f 3f', 'in_position', 'in_normal', 'texture_coords', 'in_color'),
				]
			)
		# material data
		self.shader_program['transparency'].write(self.material.transparency)
		if hasattr(self.material, 'border_only'):
			self.shader_program['border_only'].write(self.material.border_only)
			self.shader_program['border_size'].write(self.material.border_size)
			self.shader_program['border_color'].write(self.material.border_color)
		# disable next render update
		self.should_update = False

	def destroy(self):
		self.vbo.release()
		self.vao.release()

class MeshInstanced(Mesh):
	def __init__(
		self,
		geometry,
		material,
		shader_program,
		instance_data,
		update_method = None,
	):
		# setup mesh
		super().__init__(geometry, material, shader_program, update_method)
		# setup sintanced data
		self.instance_data = instance_data

	def get_model_matrix(self, instance_index = 0):
		# instnce data
		position = self.instance_data[instance_index].get('position') or self.geometry.position
		rotation = self.instance_data[instance_index].get('rotation') or self.geometry.rotation
		scale = self.instance_data[instance_index].get('scale') or self.geometry.scale
		# matrices
		translation_matrix = glm.translate(glm.mat4(1.0), glm.vec3(*position))
		rotation_quaternion = glm.quat(glm.radians(rotation))
		rotation_matrix = glm.mat4_cast(rotation_quaternion)
		scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(*scale))
		# model matrix
		model = translation_matrix * rotation_matrix * scale_matrix
		return model

	def render(self, projection, view, ctx, render_mode):
		# update callback
		if isinstance(self.update_method, list):
			for update_method in self.update_method:
				if callable(update_method):
					update_method(self.geometry, self.material, self.instance_data)
		elif callable(self.update_method):
			self.update_method(self.geometry, self.material, self.instance_data)

		# get combined vertex data
		self.setup_vertex_data()
		# update vertices
		self.update(ctx)
		# mvp
		self.shader_program['projection'].write(projection)
		self.shader_program['view'].write(view)
		# render each isntance
		for instance_index in range(len(self.instance_data)):
			model_matrix = self.get_model_matrix(instance_index)
			self.shader_program['model'].write(model_matrix)
			self.shader_program['instance_index'].write(glm.float_(instance_index / len(self.instance_data)))
			# render
			self.vao.render(render_mode, instances = 1)

