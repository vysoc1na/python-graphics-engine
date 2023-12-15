import glm

from src.core.mesh import Mesh, MeshComponent

from src.components.cursor import Cursor

class Chunk():
	def __init__(
		self,
		app,
		config,
		name = 'chunk',
		position = [0, 0, 0],
		size = 10,
	):
		self.app = app
		self.config = config
		self.name = name
		self.size = size

		self.components = {}
		self.children = {}

		self.set_position(position)
		self.is_mounted = False

	def mount(self):
		if self.is_mounted == True:
			return

		# make renderable vao's for individual mesh components
		components = self.config['components']
		for component in components:
			self.components[component['name']] = MeshComponent(
				app = self.app,
				shader_program = self.app.shader_program.programs[component['shader']],
				name = component['name'],
				parent = self.get_or(component, 'parent', None),
			)
		# compose all children for scene to render
		children = self.config['children']
		for item in children:
			# update position relative to chunk position
			position = glm.vec3(self.get_or(item, 'position', [0, 0, 0]))
			position.x += self.position.x * self.size
			position.z += self.position.z * self.size
			mesh_constructor = Mesh(
				app = self.app,
				mesh_component = self.components[item['type']],
				name = item['name'],
				position = position,
				scale = self.get_or(item, 'scale', [1, 1, 1]),
				color = self.get_or(item, 'color', None),
			)
			self.children[item['name']] = self.assign_mesh_parent(mesh_constructor)

		# debug tiles
		#n, s = 10, 1
		#for x in range(-n, n, s):
		#	for z in range(-n, n, s):
		#		position = glm.vec3(x, 0, z)
		#		position.x += self.position.x * self.size
		#		position.z += self.position.z * self.size
		#		self.children[f'debug|{x},{z}'] = Mesh(
		#			app = self.app,
		#			mesh_component = self.components['leaf'],
		#			position = position,
		#			scale = [0.2, 0.2, 0.2]
		#		)

		self.is_mounted = True

	def render(self):
		if self.is_mounted == False:
			return

		for _, key in enumerate(self.children):
			self.children[key].render()

	def destroy(self):
		if self.is_mounted == False:
			return

		for _, key in enumerate(self.children):
			self.children[key].destroy()

		self.components.clear()
		self.children.clear()

		self.is_mounted = False

	def set_position(self, position):
		self.position = glm.vec3(position)

	@staticmethod
	def get_or(item, key, default):
		if key in item:
			return item[key]
		else:
			return default

	def assign_mesh_parent(self, mesh_constructor):
		if mesh_constructor.mesh.parent == 'cursor':
			return Cursor(self.app, mesh_constructor)

		return mesh_constructor

	def get_depth(self, x, y):
		depth_attachment = self.app.ctx.depth_texture((self.app.window_size[0], self.app.window_size[1]))
		fbo = self.app.ctx.framebuffer(depth_attachment = depth_attachment)
		fbo.clear()
		fbo.use()

		self.render()

		depth_data = fbo.read(components = 1, dtype = 'f4', attachment = -1)
		depth_array = np.frombuffer(depth_data, dtype=np.float32)

		normalized_depth = (depth_array - np.min(depth_array)) / (np.max(depth_array) - np.min(depth_array))
		clipped_depth = np.clip(normalized_depth, 0, 1)
		depth_data_flipped = np.flipud(clipped_depth.reshape((self.app.window_size[1], self.app.window_size[0])))

		return depth_data_flipped[y - 1, x - 1]
