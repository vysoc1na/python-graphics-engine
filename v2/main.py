from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
# from core.geometry import BoxGeometry, PlaneGeometry, TerrainPlaneGeometry
# from core.material import SolidMaterial
# from core.mesh import Mesh, MeshInstanced
from components.terrain import Terrain
from components.player import Player

renderer = Renderer()

scene = Scene(renderer)
camera = Camera(renderer)

# Box Geometry
"""
def box_update_method(geometry, material):
	geometry.rotation.x += 10 / renderer.delta_time
	geometry.rotation.y += 10 / renderer.delta_time

box_mesh = Mesh(
	geometry = BoxGeometry(),
	material = SolidMaterial(color = (0.6, 0.3, 0.5)),
	shader_program = renderer.shaders['default'],
	update_method = box_update_method,
)
scene.children.append(box_mesh)
"""

# BoxGeoemtry Instanced Example
"""
def box_update_method(geometry, material, instance_data):
	geometry.rotation.x += 10 / renderer.delta_time
	geometry.rotation.y += 10 / renderer.delta_time

instance_data = []
for y in range(50):
	for x in range(50):
		instance_data.append({ 'position': [x * 1.5 - 37.5, y * 1.5 - 37.5, -90] })

box_mesh = MeshInstanced(
	geometry = BoxGeometry(),
	material = SolidMaterial(color = (1, 0.8, 0.7)),
	shader_program = renderer.shaders['default'],
	update_method = box_update_method,
	instance_data = instance_data,
)
scene.children.append(box_mesh)
"""

# PlaneGeometry Example
"""
plane_mesh = Mesh(
	geometry = PlaneGeometry(rotation = (45, 0, 0)),
	material = SolidMaterial(color = (1, 0, 0)),
	shader_program = renderer.shaders['default'],
)
scene.children.append(plane_mesh)
"""

# Terrain
terrain = Terrain(renderer)
scene.children.append(terrain.mesh)
# Player Entity
player = Player(renderer, terrain_component = terrain, camera_component = camera)
scene.children.append(player.mesh)

renderer.run(scene, camera)
