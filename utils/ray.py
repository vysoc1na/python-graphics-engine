import glm

def get_ray_direction(renderer, camera_component, mouse_position):
	width = renderer.config['width']
	height = renderer.config['height']

	mouse_x, mouse_y = mouse_position
	near_point = glm.vec3(mouse_x, height - mouse_y, 0)
	far_point = glm.vec3(mouse_x, height - mouse_y, 1)

	m_view = camera_component.m_view
	m_projection = camera_component.m_projection
	viewport = (0, 0, width, height)

	near_world = glm.unProject(near_point, m_view, m_projection, viewport)
	far_world = glm.unProject(far_point, m_view, m_projection, viewport)

	return glm.normalize(far_world - near_world)

def ray(renderer, camera_component, height_map, mouse_position):
	ray_origin = camera_component.position
	ray_direction = get_ray_direction(
		renderer,
		camera_component,
		mouse_position,
	)

	plane_height = 0.0

	ray_direction = glm.normalize(ray_direction)
	t = (plane_height - ray_origin.y) / ray_direction.y
	intersection_point = ray_origin + t * ray_direction

	grid_x = int(intersection_point.x)
	grid_z = int(intersection_point.z)

	grid_x = max(0, min(grid_x, len(height_map[0]) - 1))
	grid_z = max(0, min(grid_z, len(height_map) - 1))

	intersection_point.y = height_map[grid_z][grid_x]

	return intersection_point
