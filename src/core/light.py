import glm

class Light():
	def __init__(self, position = (0, 0, -5), color = (1, 1, 1)):
		self.position = glm.vec3(position)
		self.color = glm.vec3(color)

		# intensity
		self.Ia = self.color * 0.4 # ambient,  default: 0.1
		self.Id = self.color * 1.0 # diffuse,  default: 0.8
		self.Is = self.color * 0.0 # specular, default: 1.0
