import glm

class SolidMaterial():
	def __init__(
		self,
		color = (1, 1, 1),
		transparency = 1,
	):
		# setup config
		self.color = glm.vec3(color)
		self.transparency = glm.float_(transparency)

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
