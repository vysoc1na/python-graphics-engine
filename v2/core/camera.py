import glm

class Camera():
	def __init__(self, renderer):
		# setup context
		self.renderer = renderer
		self.ctx = renderer.ctx
		# setup mvp
		self.setup_mvp()

	def setup_mvp(self):
		# constants
		fov = glm.radians(45.0)
		aspect_ratio = self.renderer.config['width'] / self.renderer.config['height']
		near_plane = 0.1
		far_plane = 100
		# mvp
		self.m_projection = glm.perspective(fov, aspect_ratio, near_plane, far_plane)
		self.m_view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
		self.m_model = glm.mat4(1.0)
