from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.geometry import BoxGeometry, PlaneGeometry
from core.material import SolidMaterial
from core.mesh import Mesh, MeshInstanced

renderer = Renderer()

scene = Scene(renderer)
camera = Camera(renderer)

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
	geometry = PlaneGeometry(),
	material = SolidMaterial(color = (1, 0, 0)),
	shader_program = renderer.shaders['default'],
)
scene.children.append(plane_mesh)
"""

renderer.run(scene, camera)
