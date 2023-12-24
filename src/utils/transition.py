import glm

TRANSITION_ERROR_MARGIN = 0.01

def transition_vec3(original_value, new_value, delta_time, duration):
	if original_value == None:
		return None

	diff = glm.length(new_value - original_value)
	if diff < TRANSITION_ERROR_MARGIN:
		return new_value

	return original_value + (new_value - original_value) * (delta_time / duration)

def transition_float(original_value, new_value, delta_time, duration):
	if original_value == None:
		return None

	diff = new_value - original_value
	if abs(diff) < TRANSITION_ERROR_MARGIN:
		return new_value

	return original_value + (new_value - original_value) * (delta_time / duration)
