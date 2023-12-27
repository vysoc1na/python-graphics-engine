import pywavefront
import json

def get_vertex_data(path):
	objs = pywavefront.Wavefront(path, cache = False, parse = True)
	data = {}

	for name, item in objs.materials.items():
		data[name] = {
			'color': [item.diffuse[0], item.diffuse[1], item.diffuse[2]],
			'vertices': item.vertices,
		}

	return data

def save_json(name, data):
	file = open(f'models/{name}.json', 'w', encoding = 'utf-8')
	file.write(json.dumps(data))
	file.close()

print('Waiting for inputs...')

file_path = input('path: ')
name = input('name: ')
description = input('description: ')

print('Converting obj to vertex data...')

vertex_data = get_vertex_data(file_path)

print('Modeling json structure...')

json_data = {
	'meta': {
		'name': name,
		'description': description,
	},
	'components': []
}

for _, key in enumerate(vertex_data):
	json_data['components'].append({
		'name': f'{name}/{key}',
		'color': vertex_data[key]['color'],
		'vertex_data': vertex_data[key]['vertices']
	})

print(f'Saving json file to models/{name}.json')

save_json(name, json_data)

print('Job done!')
