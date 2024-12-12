// 3-dots-fade.svg generation

var spinnerSVG = document.createElementNS("http://www.w3.org/2000/svg", 'svg');
spinnerSVG.setAttribute('width', '24');
spinnerSVG.setAttribute('height', '24');
spinnerSVG.setAttribute('viewBox', '0 0 24 24');

spinnerSVG.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'circle'));
spinnerSVG.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'circle'));
spinnerSVG.appendChild(document.createElementNS("http://www.w3.org/2000/svg", 'circle'));

spinnerSVG.childNodes[0].classList.add('spinner_S1WN');
spinnerSVG.childNodes[0].setAttribute('cx', '4');
spinnerSVG.childNodes[0].setAttribute('cy', '12');
spinnerSVG.childNodes[0].setAttribute('r', '3');
spinnerSVG.childNodes[0].setAttribute('fill', 'white');

spinnerSVG.childNodes[1].classList.add('spinner_S1WN', 'spinner_Km9P');
spinnerSVG.childNodes[1].setAttribute('cx', '12');
spinnerSVG.childNodes[1].setAttribute('cy', '12');
spinnerSVG.childNodes[1].setAttribute('r', '3');
spinnerSVG.childNodes[1].setAttribute('fill', 'white');

spinnerSVG.childNodes[2].classList.add('spinner_S1WN', 'spinner_JApP');
spinnerSVG.childNodes[2].setAttribute('cx', '20');
spinnerSVG.childNodes[2].setAttribute('cy', '12');
spinnerSVG.childNodes[2].setAttribute('r', '3');
spinnerSVG.childNodes[2].setAttribute('fill', 'white');

// 3-dots-fade.svg usage
var loginButton = document.getElementById('login-button');

function checkLogin() {
	// show spinner on click
	loginButton.innerHTML = '';
	loginButton.appendChild(spinnerSVG);
	
	// check if the form values are valid
	var formData = $('form').serializeArray();
	let username = formData[0]['value'];
	let password = formData[1]['value'];
	
	var formPrompt = document.getElementById("form-prompt");
	
	if (username !== '' && password !== '') {
		// check if the password is 8 or more characters long
		if (password.length >= 8) {
			// assume it's an email address entered
			if (username.includes('@')) {
				// check if it's an actual valid email address
				if (validateEmail(username)) {
					// submit form
					$('form').submit();
				} else {
					// so... it's not a valid email address
					document.getElementsByName("username")[0].classList.add('invalid');
					document.getElementsByName("password")[0].classList.remove('invalid');
					
					if (formPrompt.getElementsByTagName('p').length == 0) {
						formPrompt.appendChild(document.createElement('p'));
					}
					formPrompt.childNodes[0].innerHTML = "Invalid email address entered. Please try again.";
					formPrompt.classList.add('dialog', 'error');
					addIcons();
					
					loginButton.removeChild(spinnerSVG);
					loginButton.innerHTML = "SIGN IN";
					
					console.log("invalid email");
				}
			} else {
				// ig it's a username then
				$('form').submit();
			}
		} else {
			// password is too short
			document.getElementsByName("password")[0].classList.add('invalid');
			document.getElementsByName("username")[0].classList.remove('invalid');
			
			if (formPrompt.getElementsByTagName('p').length == 0) {
				formPrompt.appendChild(document.createElement('p'));
			}
			formPrompt.childNodes[0].innerHTML = "Invalid password entered. Must be 8 or more characters long. Please try again.";
			formPrompt.classList.add('dialog', 'error');
			addIcons();
			
			loginButton.removeChild(spinnerSVG);
			loginButton.innerHTML = "SIGN IN";
			
			console.log("invalid pass");
		}
	} else {
		if (username == '' && password != '') {
			// username/email address missing
			document.getElementsByName("username")[0].classList.add('invalid');
			document.getElementsByName("password")[0].classList.remove('invalid');
			
			if (formPrompt.getElementsByTagName('p').length == 0) {
				formPrompt.appendChild(document.createElement('p'));
			}
			formPrompt.childNodes[0].innerHTML = "No username or email address entered. Please enter one.";
			formPrompt.classList.add('dialog', 'error');
			addIcons();
			
			loginButton.removeChild(spinnerSVG);
			loginButton.innerHTML = 'SIGN IN';
		} else if (username != '' && password == '') {
			// password missing
			document.getElementsByName("password")[0].classList.add('invalid');
			document.getElementsByName("username")[0].classList.remove('invalid');
			
			if (formPrompt.getElementsByTagName('p').length == 0) {
				formPrompt.appendChild(document.createElement('p'));
			}
			formPrompt.childNodes[0].innerHTML = "Password required. Please enter one.";
			formPrompt.classList.add('dialog', 'error');
			addIcons();
			
			loginButton.removeChild(spinnerSVG);
			loginButton.innerHTML = 'SIGN IN';
		} else {
			// bruh pls attempt an actual login for at least once
			document.getElementsByName("username")[0].classList.add('invalid');
			document.getElementsByName("password")[0].classList.add('invalid');
			
			if (formPrompt.getElementsByTagName('p').length == 0) {
				formPrompt.appendChild(document.createElement('p'));
			}
			formPrompt.childNodes[0].innerHTML = "Please enter your login details.";
			formPrompt.classList.add('dialog', 'error');
			addIcons();
			
			loginButton.removeChild(spinnerSVG);
			loginButton.innerHTML = 'SIGN IN';
		}
	}
}

function validateEmail (email) {
	return email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
}