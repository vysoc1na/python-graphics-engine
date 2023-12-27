import heapq
import numpy as np

def heuristic(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def tie_breaking(a, b, start):
	straight_line_distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
	start_distance = abs(a[0] - start[0]) + abs(a[1] - start[1])

	return straight_line_distance - 0.5 * start_distance

def astar(obstacles, start, end, limit = 100):
	obstacles = np.array(obstacles)
	obstacles = tuple(map(tuple, obstacles))

	if end in obstacles:
		return None

	open_set = []
	heapq.heappush(open_set, (0, start))

	came_from = {}
	cost_so_far = {start: 0}

	while open_set:
		current_cost, current_node = heapq.heappop(open_set)

		if current_node == end:
			path = reconstruct_path(came_from, start, end, limit)
			return path

		for next_node in neighbors(obstacles, current_node):
			if current_node[0] != next_node[0] and current_node[1] != next_node[1]:
				new_cost = cost_so_far[current_node] + 1.5
			else:
				new_cost = cost_so_far[current_node] + 1

			if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
				cost_so_far[next_node] = new_cost
				priority = new_cost + heuristic(end, next_node) + tie_breaking(current_node, next_node, start)
				heapq.heappush(open_set, (priority, next_node))
				came_from[next_node] = current_node

	return None

def neighbors(obstacles, node):
	x, y = node
	potential_neighbors = [
		(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
		# (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)
	]
	valid_neighbors = []

	for i, j in potential_neighbors:
		if (i, j) not in obstacles:
			if (i != x and j != y) and ((i, y) not in obstacles and (x, j) not in obstacles):
				valid_neighbors.append((i, j))
			elif i == x or j == y:
				valid_neighbors.append((i, j))

	return valid_neighbors

def reconstruct_path(came_from, start, end, limit):
	current = end
	path = []

	while current != start:
		path.append(current)
		current = came_from[current]

	if start in path:
		path.remove(start)

	path.reverse()
	return path[:limit]
