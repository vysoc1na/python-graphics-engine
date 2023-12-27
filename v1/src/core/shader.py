class ShaderProgram():
	def __init__(self, ctx):
		self.ctx = ctx
		self.programs = {}
		self.programs['default'] = self.get_program('default')

	def get_program(self, name):
		with open(f'src/shaders/{name}.vert') as file:
			vertexShader = file.read()

		with open(f'src/shaders/{name}.frag') as file:
			fragmentShader = file.read()

		program = self.ctx.program(vertex_shader = vertexShader, fragment_shader = fragmentShader)
		return program

	def destroy(self):
		[program.release() for program in self.programs.values()]
