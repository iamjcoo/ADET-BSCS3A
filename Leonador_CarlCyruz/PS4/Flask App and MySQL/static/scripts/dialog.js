var dialogIconPaths = {};
dialogIconPaths["warning"] = "M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2";
dialogIconPaths["success"] = "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z";
dialogIconPaths["info-seg1"] = "M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16";
dialogIconPaths["info-seg2"] = "m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0";
dialogIconPaths["error"] = "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z";

const dialogIcon = document.createElementNS("http://www.w3.org/2000/svg", 'svg');
dialogIcon.setAttribute('width', '16');
dialogIcon.setAttribute('height', '16');
dialogIcon.setAttribute('fill', 'currentColor');
dialogIcon.setAttribute('viewBox', '0 0 16 16');
dialogIcon.classList.add(['bi']);

function addIcons() {
	var dialogs = document.getElementsByClassName('dialog');

	if (dialogs.length == 0) {
		return;
	}

	for (let dialog of dialogs) {
		let selectedIcon;
		if (dialog.classList.contains('warning')) {
			let warningIcon = dialogIcon.cloneNode(true);
			warningIcon.classList.add(['bi-exclamation-triangle-fill']);		
			warningIcon.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'path'));
			warningIcon.childNodes[0].setAttribute('d', dialogIconPaths['warning']);

			selectedIcon = warningIcon;
		} else if (dialog.classList.contains('success')) {
			let successIcon = dialogIcon.cloneNode(true);
			successIcon.classList.add(['bi-check-circle-fill']);
			successIcon.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'path'));
			successIcon.childNodes[0].setAttribute('d', dialogIconPaths['success']);

			selectedIcon = successIcon;
		} else if (dialog.classList.contains('info')) {
			let infoIcon = dialogIcon.cloneNode(true);
			infoIcon.classList.add(['bi-info-circle']);
			infoIcon.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'path'));
			infoIcon.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'path'));
			infoIcon.childNodes[0].setAttribute('d', dialogIconPaths['info-seg1']);
			infoIcon.childNodes[1].setAttribute('d', dialogIconPaths['info-seg2']);

			selectedIcon = infoIcon;
		} else if (dialog.classList.contains('error')) {
			let errorIcon = dialogIcon.cloneNode(true);
			errorIcon.classList.add(['bi-x-circle-fill']);
			errorIcon.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'path'));
			errorIcon.childNodes[0].setAttribute('d', dialogIconPaths['error']);

			selectedIcon = errorIcon;
		}

		if (dialog.getElementsByTagName('p').length == 1) {
			if (dialog.children[0].getElementsByTagName('svg').length == 0) {
				dialog.children[0].insertBefore(selectedIcon, dialog.children[0].childNodes[0]);
			}
		}
	}
	return;
}

addIcons();