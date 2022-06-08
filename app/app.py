from copy import deepcopy
from glob import glob
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
from uuid import uuid4

from flask import Flask, render_template, request, send_file
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def int_to_float(graph):
	if isinstance(graph, dict):
		if 'camera' in graph:
			graph['camera']['position'] = list(map(float, graph['camera']['position']))
			graph['camera']['up'] = list(map(float, graph['camera']['up']))
			graph['camera']['view'] = list(map(float, graph['camera']['view']))

		if 'subType' in graph.keys():
			_type = graph['subType']
			if _type == 'float':
				graph['value'] = float(graph['value'])
			if _type == 'rgb' or \
				(_type.startswith('vec') and _type.endswith('f')):
				graph['value'] = list(map(float, graph['value']))
			if _type.startswith('quaternion') and _type.endswith('f'):
				for key in graph['value']:
					graph['value'][key] = float(graph['value'][key])
		for key in graph:
			int_to_float(graph[key])
	if isinstance(graph, list):
		for item in graph:
			int_to_float(item)


# linear interpolation of all frame properties
def interpolate(frame1, frame2):  # pylint: disable=too-many-branches
	if isinstance(frame1, dict):
		if 'camera' in frame1:
			frame1['camera']['position'] = list(map(lambda x, y: float((x + y) / 2), frame1['camera']['position'], frame2['camera']['position']))  # noqa: E501
			frame1['camera']['up'] = list(map(lambda x, y: float((x + y) / 2), frame1['camera']['up'], frame2['camera']['up']))  # noqa: E501
			frame1['camera']['view'] = list(map(lambda x, y: float((x + y) / 2), frame1['camera']['view'], frame2['camera']['view']))  # noqa: E501

		if 'subType' in frame1.keys():
			_type = frame1['subType']
			if _type == 'float':
				frame1['value'] = float((frame1['value'] + frame2['value']) / 2)
			if _type == 'rgb' or \
				(_type.startswith('vec') and _type.endswith('f')):
				frame1['value'] = list(map(lambda x, y: float((x + y) / 2), frame1['value'], frame2['value']))  # noqa: E501
			if _type.startswith('vec') and _type.endswith('i'):
				frame1['value'] = list(map(lambda x, y: (x + y) // 2, frame1['value'], frame2['value']))  # noqa: E501
			if _type.startswith('quaternion') and _type.endswith('f'):
				for key in frame1['value']:
					frame1['value'][key] = float((frame1['value'][key] + frame2['value'][key]) / 2)  # noqa: E501
			if _type.startswith('quaternion') and _type.endswith('i'):
				for key in frame1['value']:
					frame1['value'][key] = (frame1['value'][key] + frame2['value'][key]) // 2  # noqa: E501
		for key in frame1:
			interpolate(frame1[key], frame2[key])
	if isinstance(frame1, list):
		for item1, item2 in zip(frame1, frame2):
			interpolate(item1, item2)


def get_frame(
	camera,
	filename,
	scene_graph=None,
	movie=False,
	extra_args=None
):
	if extra_args is None:
		extra_args = []

	if scene_graph is not None:
		sg_filename = uuid4().hex + '.sg'
		with open(sg_filename, 'w', encoding='utf-8') as _file:
			json.dump(scene_graph, _file)

		extra_args.append(sg_filename)

	args = [
		'/opt/build/ospray_studio/build/ospStudio',
		'batch',
		'--denoiser',
		'--position',
		str(camera['position'][0]),
		str(camera['position'][1]),
		str(camera['position'][2]),
		'--up',
		str(camera['up'][0]),
		str(camera['up'][1]),
		str(camera['up'][2]),
		'--view',
		str(camera['view'][0]),
		str(camera['view'][1]),
		str(camera['view'][2]),
		'--image',
		filename
	]

	if scene_graph is not None:
		if 'resolution' in scene_graph:
			args.append('--resolution')
			args.append(str(scene_graph.get('resolution', '720p')))

		if 'samples_per_pixel' in scene_graph:
			args.append('--spp')
			args.append(str(scene_graph.get('samples_per_pixel', 1)))

	if not movie:
		args.append('--forceRewrite')

	if not Path('studio_scene.sg').exists():
		args.append('--saveScene')

	subprocess.run(args + extra_args, check=True)

	if scene_graph is not None:
		os.remove(sg_filename)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/render/', methods=['GET', 'POST'])
def render():
	image_filename = uuid4().hex

	if request.method == 'GET':
		data_files = []
		for root, _, filenames in os.walk('/data'):
			for _file in filenames:
				if _file.endswith(('.gltf', '.obj')):
					data_files.append(os.path.join(root, _file))

		get_frame({
			'position': [0.0, 0.0, 1.0],
			'up': [0.0, 1.0, 0.0],
			'view': [0.0, 0.0, -1.0],
		}, image_filename, extra_args=data_files)
	else:
		scene_graph = request.json
		int_to_float(scene_graph)

		get_frame(scene_graph['camera'], image_filename, scene_graph=scene_graph)

	with open(f'{image_filename}.00000.png', 'rb') as image:
		image_data = BytesIO(image.read())

	os.remove(f'{image_filename}.00000.png')

	return send_file(image_data, mimetype='image/png')


@app.route('/renderMovie/', methods=['POST'])
def render_movie():
	image_filename = uuid4().hex
	data = request.json

	fps = int(data.get('fps', 30))
	length = int(data.get('length', 10))

	keyframes = data.get('frames', [])
	for frame in keyframes:
		int_to_float(frame)

	frames = keyframes
	while len(frames) < fps * length:
		frame_index = len(frames) - 1
		while frame_index > 0 and len(frames) < fps * length:
			new_frame = deepcopy(frames[frame_index - 1])
			interpolate(new_frame, frames[frame_index])

			frames = frames[:frame_index] + [new_frame] + frames[frame_index:]
			frame_index -= 1

	for scene_graph in frames:
		camera = {
			'position': list(map(float, scene_graph['camera']['position'])),
			'up': list(map(float, scene_graph['camera']['up'])),
			'view': list(map(float, scene_graph['camera']['view']))
		}

		get_frame(camera, image_filename, scene_graph=scene_graph, movie=True)

	subprocess.run([
		'/opt/build/ffmpeg/ffmpeg',
		'-i',
		f'{image_filename}.%05d.png',
		'-c:v',
		'libsvtav1',
		'-r',
		str(fps),
		f'{image_filename}.mp4'
	], check=True)

	with open(f'{image_filename}.mp4', 'rb') as video:
		video_data = BytesIO(video.read())

	for _file in glob(f'{image_filename}*'):
		os.remove(_file)

	return send_file(video_data, mimetype='video/mp4')


@app.route('/sg/')
def scenegraph():
	with open('studio_scene.sg', 'r', encoding='utf-8') as _file:
		return json.load(_file)
