import numpy as np
import glm
import heapq

def heuristic(a, b):
	return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

def get_neighbors(node, obstacles):
	neighbors = []
	for dir in [
		(1, 0), (0, 1), (-1, 0), (0, -1),
		(1, 1), (1, -1), (-1, 1), (-1, -1)
	]:
		neighbor = (node[0] + dir[0], node[1] + dir[1])
		if neighbor not in obstacles:
			neighbors.append(neighbor)
	return neighbors

def astar(obstacles, start, end):
	start = tuple(start)
	end = tuple(end)

	if start == end or end in obstacles:
		return []

	open_set = []
	heapq.heappush(open_set, (0, start))

	came_from = {}
	cost_so_far = {start: 0}

	while open_set:
		current = heapq.heappop(open_set)[1]

		if current == end:
			path = []
			while current in came_from:
				path.append(current)
				current = came_from[current]
			return path[::-1]

		for neighbor in get_neighbors(current, obstacles):
			new_cost = cost_so_far[current] + 1
			if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
				cost_so_far[neighbor] = new_cost
				priority = new_cost + heuristic(end, neighbor)
				heapq.heappush(open_set, (priority, neighbor))
				came_from[neighbor] = current

	return []
