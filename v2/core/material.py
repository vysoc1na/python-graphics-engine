import glm

class SolidMaterial():
	def __init__(
		self,
		color = (1, 1, 1),
		transparency = 1,
		border_only = False,
		border_size = 0,
		border_color = 0,
	):
		# setup config
		self.color = glm.vec3(color)
		self.transparency = glm.float_(transparency)
		# borders
		self.border_only = glm.bool_(border_only)
		self.border_size = glm.float_(border_size)
		self.border_color = glm.vec3(border_color)

class TerrainMaterial():
	def __init__(
		self,
		color_low = (0, 0, 0),
		color_high = (1, 1, 1),
		transparency = 1,
	):
		self.color_low = glm.vec3(color_low)
		self.color_high = glm.vec3(color_high)
		self.transparency = glm.float_(transparency)
