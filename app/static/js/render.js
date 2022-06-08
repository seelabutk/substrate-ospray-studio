function render(scene_graph) {
	const spinner = document.querySelector('.spinner');
	spinner.style.display = 'block';

	const options = {};
	if (scene_graph !== undefined) {
		options.body = JSON.stringify(scene_graph);
		options.headers = {'Content-Type': 'application/json'};
		options.method = 'POST';
	}

	fetch('/render/', options).then((response) => response.blob()).then((blob) => {
		const image_url = URL.createObjectURL(blob);

		const image = document.querySelector('.render');
		image.src = image_url;

		spinner.style.display = 'none';

		if (scene_graph === undefined) {
			fetch('/sg/').then((response) => response.json()).then((sg) => {
				sg.camera.position = [0.0, 0.0, 1.0];
				sg.camera.up = [0.0, 1.0, 0.0];
				sg.camera.view = [0.0, 0.0, -1.0];
				sg.samples_per_pixel = 16;
				sg.resolution = '1080p';

				SGEDITOR.set(sg);
			});
		}
	});
}
