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

