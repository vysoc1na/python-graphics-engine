import glm

def ray(ray_origin, ray_direction, height_map):
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
