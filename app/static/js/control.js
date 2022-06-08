let SGEDITOR = null;

function setupSGEditor(json) {
	const container = document.querySelector('.sg-editor');
	SGEDITOR = new JSONEditor(container, {});
}
