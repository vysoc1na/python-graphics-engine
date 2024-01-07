import colorsys
import numpy

def brighten(color, factor):
	original_color = numpy.array(color)
	brighter_color = original_color * factor

	return tuple(numpy.clip(brighter_color, 0, 1))

def saturate(color, factor):
	hsv_color = colorsys.rgb_to_hsv(*color)

	adjusted_saturation = numpy.clip(hsv_color[1] * factor, 0, 1)
	adjusted_rgb_color = colorsys.hsv_to_rgb(hsv_color[0], adjusted_saturation, hsv_color[2])

	return tuple(numpy.array(adjusted_rgb_color))
