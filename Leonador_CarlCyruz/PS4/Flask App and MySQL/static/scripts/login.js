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

spinnerSVG.childNodes[1].classList.add('spinner_S1WN', 'spinner_Km9P');
spinnerSVG.childNodes[1].setAttribute('cx', '12');
spinnerSVG.childNodes[1].setAttribute('cy', '12');
spinnerSVG.childNodes[1].setAttribute('r', '3');

spinnerSVG.childNodes[2].classList.add('spinner_S1WN', 'spinner_JApP');
spinnerSVG.childNodes[2].setAttribute('cx', '20');
spinnerSVG.childNodes[2].setAttribute('cy', '12');
spinnerSVG.childNodes[2].setAttribute('r', '3');

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
		// assume the entered text is an email address
		if (username.includes('@')) {
			// check if it's an actual valid email address
			if (validateEmail(username)) {
				if (password.length >= 8) {
					$('form').submit();
				} else {
					document.getElementsByName("password")[0].classList.add('invalid');
					
					formPrompt.appendChild(document.createElement('p'));
					formPrompt.childNodes[0].innerHTML = "Invalid password entered. Please try again.";
					formPrompt.classList.add('dialog', 'error');
					
					loginButton.removeChild(spinnerSVG);
					loginButton.innerHTML = "LOGIN";
					
					console.log("invalid pass");
				}
			}
		} else {
			if (password.length >= 8) {
				$('form').submit();
			} else {
				document.getElementsByName("password")[0].classList.add('invalid');
				
				formPrompt.appendChild(document.createElement('p'));
				formPrompt.childNodes[0].innerHTML = "Invalid password entered. Please try again.";
				formPrompt.classList.add('dialog', 'error');
				
				loginButton.removeChild(spinnerSVG);
				loginButton.innerHTML = "LOGIN";
				
				console.log("invalid pass");
			}
		}
	} else {
		if (username == '' && password != '') {
			document.getElementsByName("username")[0].classList.add('invalid');
			document.getElementsByName("password")[0].classList.remove('invalid');
			
			formPrompt.appendChild(document.createElement('p'));
			formPrompt.childNodes[0].innerHTML = "No username or email address entered. Please enter one.";
			formPrompt.classList.add('dialog', 'error');
			
			loginButton.removeChild(spinnerSVG);
			loginButton.innerHTML = 'LOGIN';
		} else if (username != '' && password == '') {
			document.getElementsByName("password")[0].classList.add('invalid');
			document.getElementsByName("username")[0].classList.remove('invalid');
			
			formPrompt.appendChild(document.createElement('p'));
			formPrompt.childNodes[0].innerHTML = "Password required. Please enter one.";
			formPrompt.classList.add('dialog', 'error');
			
			loginButton.removeChild(spinnerSVG);
			loginButton.innerHTML = 'LOGIN';
		} else {
			document.getElementsByName("username")[0].classList.add('invalid');
			document.getElementsByName("password")[0].classList.add('invalid');
			
			formPrompt.appendChild(document.createElement('p'));
			formPrompt.childNodes[0].innerHTML = "Please enter your login details.";
			formPrompt.classList.add('dialog', 'error');
			
			loginButton.removeChild(spinnerSVG);
			loginButton.innerHTML = 'LOGIN';
		}
	}
}

function validateEmail (email) {
	return email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
}