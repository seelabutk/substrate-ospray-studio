const RAAS_LOCATION = 'http://172.19.54.56:8000';

function initial_render() {
	fetch(`${RAAS_LOCATION}/render/`).then((response) => response.blob()).then((blob) => {
		document.querySelector('.render').src = URL.createObjectURL(blob);
	});
}

function get_scene_graph() {
	fetch(`${RAAS_LOCATION}/sg/`).then((response) => response.json()).then((scene_graph) => {
		// NOTE: Keep these three lines or camera manipulations won't work.
		scene_graph.camera.position = [0.0, 0.0, 1.0];
		scene_graph.camera.up = [0.0, 1.0, 0.0];
		scene_graph.camera.view = [0.0, 0.0, -1.0];
	});
}

function re_render(scene_graph) {
	const options = {
		body: JSON.stringify(scene_graph),
		headers: {'Content-Type': 'application/json'},
		method: 'POST'
	};

	fetch(`${RAAS_LOCATION}/render/`, options).then((response) => response.blob()).then((blob) => {
		document.querySelector('.render').src = URL.createObjectURL(blob);
	});
}

function render_movie(key_frames) {
	const options = {
		body: JSON.stringify({
			fps: 10,
			frames: key_frames,
			length: 2
		}),
		headers: {'Content-Type': 'application/json'},
		method: 'POST'
	};

	fetch(`${RAAS_LOCATION}/renderMovie/`, options).then((response) => response.blob()).then((blob) => {
		const movie_url = URL.createObjectURL(blob);
		// do something with the movie here!
	});
}
