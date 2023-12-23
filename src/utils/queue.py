class Queue():
	def __init__(self, app):
		self.app = app
		self.elapsed_time_since_last_action = 0
		self.time_to_single_action = 500

		self.actions = []

	def add(self, action):
		self.actions.append(action)

	def clear(self):
		self.actions = []

	def tick(self):
		self.elapsed_time_since_last_action += self.app.delta_time

		if self.elapsed_time_since_last_action > self.time_to_single_action:
			if len(self.actions) > 0:
				item = self.actions.pop(0)

				if callable(item.data):
					item.data(self.app)
				else:
					print('uncallable action:', item)

			self.elapsed_time_since_last_action = 0

class Action():
	def __init__(self, data = None):
		self.data = data
