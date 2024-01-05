import glm
import numpy

from utils.terrain_data import get_terrain_data

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

	def calculate_normal(self, vertex1, vertex2, vertex3):
		edge1 = vertex2 - vertex1
		edge2 = vertex3 - vertex1
		normal = numpy.cross(edge1, edge2)
		normal /= numpy.linalg.norm(normal)
		return normal

	def setup_vertex_data(self):
		self.vertices = []
		self.normals = []

class BoxGeometry(Geometry):
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
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[0, 0, -1],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[-1, 0, 0],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
			[0, 1, 0],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[1, 0, 0],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, 0, 1],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
			[0, -1, 0],
		], dtype = 'float32')

class PlaneGeometry(Geometry):
	def __init__(
		self,
		size = (1, 1, 1),
		position = (0, 0, 0),
		rotation = (0, 0, 0),
		scale = (1, 1, 1),
		corners = (0, 0, 0, 0)
	):
		# plane config
		self.corners = corners
		# init geometry
		super().__init__(size, position, rotation, scale)

	def get_plane_vertices(self, position = glm.vec2(0, 0), corners = (0, 0, 0, 0)):
		half_width = 0.5 * self.size.x
		half_height = 0.5 * self.size.y

		x = position.y
		z = position.x

		TL, TR, BL, BR = corners

		vertices = numpy.array([
			[-half_width + x, TL, -half_height + z],
			[half_width + x, TR, -half_height + z],
			[-half_width + x, BL, half_height + z],
			[half_width + x, TR, -half_height + z],
			[half_width + x, BR, half_height + z],
			[-half_width + x, BL, half_height + z],
		], dtype = 'float32')

		return vertices

	def get_plane_normals(self):
		normals = [[self.calculate_normal(*self.vertices[:3])] * 6]
		normals = numpy.concatenate(normals)
		return normals

	def setup_vertex_data(self):
		half_width = 0.5 * self.size.x
		half_height = 0.5 * self.size.y

		self.vertices = self.get_plane_vertices(corners = self.corners)
		# calculate normals for each triangle
		self.normals = self.get_plane_normals()

class TerrainPlaneGeometry(PlaneGeometry):
	def __init__(
		self,
		size = (1, 1, 1),
		position = (0, 0, 0),
		rotation = (0, 0, 0),
		scale = (1, 1, 1),
		height_map = [],
	):
		self.height_map = numpy.array(height_map, dtype = 'float32', order = 'C')

		super().__init__(size, position, rotation, scale)

	def setup_vertex_data(self):
		result_array = get_terrain_data(self.height_map)

		self.vertices = []
		self.normals = []

		# place plane meshes in correct coordinates
		for item in result_array:
			self.vertices.append(
				self.get_plane_vertices(item['position'], item['corners'])
			)
			normal = self.calculate_normal(*self.vertices[-1][:3])
			self.normals.append([normal] * 6)

		self.vertices = numpy.concatenate(self.vertices)
		# calculate normals for each triangle
		self.normals = numpy.concatenate(self.normals)
