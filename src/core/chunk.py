import glm

from src.core.mesh import Mesh, MeshComponent

from src.components import Cursor, Player

from src.utils.astar import astar

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
				parent = component.get('parent', None),
			)
		# compose all children for scene to render
		children = self.config['children']
		for item in children:
			# update position relative to chunk position
			position = glm.vec3(item.get('position', [0, 0, 0]))
			position.x += self.position.x * self.size + 0.5
			position.z += self.position.z * self.size + 0.5
			mesh_constructor = Mesh(
				app = self.app,
				mesh_component = self.components[item['type']],
				name = item['name'],
				position = position,
				scale = item.get('scale', [1, 1, 1]),
				color = item.get('color', None),
			)
			self.children[item['name']] = self.assign_mesh_parent(mesh_constructor)

		size = self.app.scene.config['size']
		row_index = 0
		for row in self.config['map']:
			col_index = 0
			for col in row:
				if col == 1:
					name = f'tile-{row_index},{col_index}'
					position = glm.vec3(item.get('position', [-size / 2, 0.2, size / 2]))
					position.x += self.position.x * self.size + 1 + row_index
					position.z += self.position.z * self.size - col_index
					self.children[name] = Mesh(
						app = self.app,
						mesh_component = self.components['tile'],
						name = name,
						position = position,
						transparency = 0.5,
						color = [1, 0, 0],
					)

				col_index += 1
			row_index += 1

		path = astar(self.config['map'], (0, 0), (31, 31))

		for item in path:
			name = f'tile-path-{item[0]},{item[1]}'
			position = glm.vec3(-size / 2, 0.2, size / 2)
			position.x += self.position.x * self.size + 1 + item[0]
			position.z += self.position.z * self.size - item[1]
			self.children[name] = Mesh(
				app = self.app,
				mesh_component = self.components['tile'],
				name = name,
				position = position,
				transparency = 0.5,
				color = [0, 1, 0],
			)


		# debug tiles
		#n, s = 20, 1
		#for x in range(-n, n, s):
		#	for z in range(-n, n, s):
		#		position = glm.vec3(x, 0.2, z)
		#		position.x += self.position.x * self.size
		#		position.z += self.position.z * self.size
		#		self.children[f'debug|{x},{z}'] = Mesh(
		#			app = self.app,
		#			mesh_component = self.components['leaf'],
		#			position = position,
		#			scale = [0.5, 0.5, 0.5],
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

	def check_event(self, event):
		# call events only in rendered chunks
		if self.is_mounted == False:
			return

		for _, key in enumerate(self.children):
			item = self.children[key]
			check_event_method = getattr(item, 'check_event', None)

			if callable(check_event_method):
				self.children[key].check_event(event)

	def set_position(self, position):
		self.position = glm.vec3(position)

	def assign_mesh_parent(self, mesh_constructor):
		if mesh_constructor.mesh.parent == 'model/cursor':
			return Cursor(self.app, mesh_constructor)

		if mesh_constructor.mesh.parent == 'model/player':
			return Player(self.app, mesh_constructor)

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
