import glm
import numpy

class Geometry():
	def __init__(
		self,
		size = (1, 1, 1),
		position = (0, 0, 0),
		rotation = (0, 0, 0),
		scale = (1, 1, 1)
	):
		# setup config
		self.size = glm.vec3(size)
		self.position = glm.vec3(position)
		self.rotation = glm.vec3(rotation)
		self.scale = glm.vec3(scale)
		# setup vertex data
		self.setup_vertex_data()

	def setup_vertex_data(self):
		self.vertices = []
		self.normals = []

class BoxGeometry(Geometry):
	def __init__(
		self,
		size = (1, 1, 1),
		position = (0, 0, 0),
		rotation = (0, 0, 0),
		scale = (1, 1, 1)
	):
		super().__init__(size, position, rotation, scale)

	def setup_vertex_data(self):
		self.vertices = numpy.array([
			[0.5, -0.5, 0.5],
			[0.5, 0.5, 0.5],
			[-0.5, -0.5, 0.5],
			[0.5, 0.5, 0.5],
			[-0.5, 0.5, 0.5],
			[-0.5, -0.5, 0.5],
			[0.5, -0.5, -0.5],
			[0.5, 0.5, -0.5],
			[0.5, -0.5, 0.5],
			[0.5, 0.5, -0.5],
			[0.5, 0.5, 0.5],
			[0.5, -0.5, 0.5],
			[0.5, -0.5, -0.5],
			[0.5, -0.5, 0.5],
			[-0.5, -0.5, 0.5],
			[0.5, -0.5, -0.5],
			[-0.5, -0.5, 0.5],
			[-0.5, -0.5, -0.5],
			[-0.5, -0.5, 0.5],
			[-0.5, 0.5, 0.5],
			[-0.5, 0.5, -0.5],
			[-0.5, -0.5, 0.5],
			[-0.5, 0.5, -0.5],
			[-0.5, -0.5, -0.5],
			[0.5, 0.5, -0.5],
			[0.5, -0.5, -0.5],
			[-0.5, -0.5, -0.5],
			[0.5, 0.5, -0.5],
			[-0.5, -0.5, -0.5],
			[-0.5, 0.5, -0.5],
			[0.5, 0.5, -0.5],
			[-0.5, 0.5, -0.5],
			[0.5, 0.5, 0.5],
			[-0.5, 0.5, -0.5],
			[-0.5, 0.5, 0.5],
			[0.5, 0.5, 0.5],
		], dtype = 'float32')
		self.vertices *= self.size

		self.normals = numpy.array([
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
		], dtype = 'float32')

class PlaneGeometry(Geometry):
	def __init__(
		self,
		size = (1, 1, 1),
		position = (0, 0, 0),
		rotation = (0, 0, 0),
		scale = (1, 1, 1)
	):
		super().__init__(size, position, rotation, scale)

	def setup_vertex_data(self):
		half_width = 0.5 * self.size.x
		half_height = 0.5 * self.size.y

		self.vertices = numpy.array([
			[-half_width, -half_height, 0.0],
			[half_width, -half_height, 0.0],
			[-half_width, half_height, 0.0],
			[half_width, -half_height, 0.0],
			[half_width, half_height, 0.0],
			[-half_width, half_height, 0.0],
		], dtype = 'float32')

		self.normals = numpy.array([
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
		], dtype = 'float32')
