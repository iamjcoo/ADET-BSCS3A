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
var registerButton = document.getElementById('register-button');

function checkRegister() {
	// show spinner on click
	registerButton.innerHTML = '';
	registerButton.appendChild(spinnerSVG);
	
	// check if the form values are valid
	var formData = $('form').serializeArray();
	let username = formData[0]['value'];
	let fname = formData[1]['value'];
	let lname = formData[3]['value'];
	let cnum = formData[4]['value'];
	let email = formData[5]['value'];
	let address = formData[6]['value'];
	let password = formData[7]['value'];
	let cPassword = formData[8]['value'];
	
	let agreed = false;

	if (formData[9] == null) {
		agreed = false;
	} else {
		agreed = true;
	}
	
	var formPrompt = document.getElementById("form-prompt");
	
	// check if all mandatory fields are not empty
	var mandatoryFields = [username, fname, lname, cnum, email, address];
	
	if (mandatoryFields.every((a)=>{return a!=''})) {
		// check if password entered is strong
		if (isPasswordStrong(password)) {
			// check if passwords are the same
			if (password != cPassword) {
				document.getElementsByName('username')[0].classList.remove('invalid');
				document.getElementsByName('fname')[0].classList.remove('invalid');
				document.getElementsByName('lname')[0].classList.remove('invalid');
				document.getElementsByName('cnum')[0].classList.remove('invalid');
				document.getElementsByName('email')[0].classList.remove('invalid');
				document.getElementsByName('address')[0].classList.remove('invalid');
				document.getElementsByName('password')[0].classList.add('invalid');
				document.getElementsByName('cPassword')[0].classList.add('invalid');
				
				if (formPrompt.getElementsByTagName('p').length == 0) {
					formPrompt.appendChild(document.createElement('p'));
				}
				formPrompt.childNodes[0].innerHTML = "Passwords don't match!";
				formPrompt.classList.add('dialog', 'error');
				addIcons();
				
				registerButton.removeChild(spinnerSVG);
				registerButton.innerHTML = 'SIGN UP';
			} else {
				if (validateEmail(email)) {
					if (agreed) {
						document.getElementsByName('username')[0].classList.remove('invalid');
						document.getElementsByName('fname')[0].classList.remove('invalid');
						document.getElementsByName('lname')[0].classList.remove('invalid');
						document.getElementsByName('cnum')[0].classList.remove('invalid');
						document.getElementsByName('email')[0].classList.remove('invalid');
						document.getElementsByName('address')[0].classList.remove('invalid');
						document.getElementsByName('password')[0].classList.remove('invalid');
						document.getElementsByName('cPassword')[0].classList.remove('invalid');
						document.getElementsByName('agree')[0].classList.remove('invalid');
						
						formPrompt.innerHTML = '';
						formPrompt.classList.remove('dialog', 'error');
						
						$('form').submit();
					} else {
						document.getElementsByName('username')[0].classList.remove('invalid');
						document.getElementsByName('fname')[0].classList.remove('invalid');
						document.getElementsByName('lname')[0].classList.remove('invalid');
						document.getElementsByName('cnum')[0].classList.remove('invalid');
						document.getElementsByName('email')[0].classList.remove('invalid');
						document.getElementsByName('address')[0].classList.remove('invalid');
						document.getElementsByName('password')[0].classList.remove('invalid');
						document.getElementsByName('cPassword')[0].classList.remove('invalid');
						document.getElementsByName('agree')[0].classList.add('invalid');

						if (formPrompt.getElementsByTagName('p').length == 0) {
							formPrompt.appendChild(document.createElement('p'));
						}
						formPrompt.childNodes[0].innerHTML = "Please accept the terms of service.";
						formPrompt.classList.add('dialog', 'error');
						addIcons();
						
						registerButton.removeChild(spinnerSVG);
						registerButton.innerHTML = 'SIGN UP';
					}
				} else {
					document.getElementsByName('username')[0].classList.remove('invalid');
					document.getElementsByName('fname')[0].classList.remove('invalid');
					document.getElementsByName('lname')[0].classList.remove('invalid');
					document.getElementsByName('cnum')[0].classList.remove('invalid');
					document.getElementsByName('email')[0].classList.add('invalid');
					document.getElementsByName('address')[0].classList.remove('invalid');
					document.getElementsByName('password')[0].classList.remove('invalid');
					document.getElementsByName('cPassword')[0].classList.remove('invalid');

					if (formPrompt.getElementsByTagName('p').length == 0) {
						formPrompt.appendChild(document.createElement('p'));
					}
					formPrompt.childNodes[0].innerHTML = "Invalid email entered.";
					formPrompt.classList.add('dialog', 'error');
					addIcons();
					
					registerButton.removeChild(spinnerSVG);
					registerButton.innerHTML = 'SIGN UP';
				}
			}
		} else {
			document.getElementsByName('username')[0].classList.remove('invalid');
			document.getElementsByName('fname')[0].classList.remove('invalid');
			document.getElementsByName('lname')[0].classList.remove('invalid');
			document.getElementsByName('cnum')[0].classList.remove('invalid');
			document.getElementsByName('email')[0].classList.remove('invalid');
			document.getElementsByName('address')[0].classList.remove('invalid');
			document.getElementsByName('password')[0].classList.add('invalid');
			document.getElementsByName('cPassword')[0].classList.remove('invalid');
			
			if (formPrompt.getElementsByTagName('p').length == 0) {
				formPrompt.appendChild(document.createElement('p'));
			}
			formPrompt.childNodes[0].innerHTML = "Password must be at least 8 characters long, and contains at least one number, one letter, or one unique character such as !-_#$%?.";
			formPrompt.classList.add('dialog', 'error');
			addIcons();
			
			registerButton.removeChild(spinnerSVG);
			registerButton.innerHTML = 'SIGN UP';
		}
	} else {
		document.getElementsByName('username')[0].classList.add('invalid');
		document.getElementsByName('fname')[0].classList.add('invalid');
		document.getElementsByName('lname')[0].classList.add('invalid');
		document.getElementsByName('cnum')[0].classList.add('invalid');
		document.getElementsByName('email')[0].classList.add('invalid');
		document.getElementsByName('address')[0].classList.add('invalid');
		document.getElementsByName('password')[0].classList.add('invalid');
		document.getElementsByName('cPassword')[0].classList.add('invalid');

		if (formPrompt.getElementsByTagName('p').length == 0) {
			formPrompt.appendChild(document.createElement('p'));
		}
		formPrompt.childNodes[0].innerHTML = "Please enter the required information";
		formPrompt.classList.add('dialog', 'error');
		addIcons();
		
		registerButton.removeChild(spinnerSVG);
		registerButton.innerHTML = 'SIGN UP';
	}
}

function validateEmail (email) {
	return email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
}

function isPasswordStrong (password) {
	/** For checking the password's strength.
	* NOTE: Only measures if the password is strong enough, NOT how SECURE it is.
	* @param String password Password string.
	* @return bool
	*/
	let hasSpecial = Array.from(password).some((a)=>{return ['!', '@', '#', '$', '%', '?', '.', '-', '_'].includes(a)});
	let hasUpper = Array.from(password).some((a)=>{return Array.from('ABCDEFGHIJKLMNOPQRSTUVWXYZ').includes(a)});
	let hasLower = Array.from(password).some((a)=>{return Array.from('abcdefghijklmnopqrstuvwxyz').includes(a)});
	let hasNumber = Array.from(password).some((a)=>{return Array.from('0123456789').includes(a)});
	
	if (password.length >= 8) {
		// Password strength: [###-------]
		if ([hasSpecial, hasUpper, hasLower, hasNumber].every((a)=>{return a==true})) {
			// [#########-]
			return true;
		} else if ([hasSpecial, hasUpper, hasLower, hasNumber].some((a)=>{return a==true})) {
			// [######----]
			return true;
		} else {
			// [----------]
			return false;
		}
	} else {
		return false;
	}
}