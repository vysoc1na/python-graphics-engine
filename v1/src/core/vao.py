class Vao():
	def __init__(self, app, shader_program, vertex_data):
		self.app = app
		self.ctx = app.ctx
		self.shader_program = shader_program

		self.vbo = self.get_vbo(vertex_data)
		self.vao = self.get_vao()

	def update(self, vertex_data):
		self.vbo = self.get_vbo(vertex_data)
		self.vao = self.get_vao()

	def get_vbo(self, vertex_data):
		return self.ctx.buffer(vertex_data)

	def get_vao(self):
		return self.ctx.vertex_array(
			self.shader_program,
			[(self.vbo, '2f 3f 3f', 'in_textcoord_0', 'in_normal', 'in_position')],
		)
