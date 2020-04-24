//Functions in this file can be used to interface with drop down windows
//If you want to open the dropdown on click, then you can add it to the onclick event
//If you want it to open on hover, then you can add it to the onmouseover event
/**
 * Toggle a dropdown
 * @param {string} id The ID of the dropdown to toggle. The dropdown should have that ID in html.
 */
function toggleDropdown(id) {
	let dropdown = document.getElementById(id);

	//We call the functions instead of using classList.toggle to update dropdown contents
	if (dropdown.classList.contains('hidden')) {
		openDropdown(id);
	} else {
		closeDropdown(id);
	}
}

/**
 * Close a dropdown
 * @param {string} id The ID of the dropdown to close. The dropdown should have that ID in html.
 */
function closeDropdown(id) {
	//Get and hide the element
	let dropdown = document.getElementById(id);
	dropdown.classList.add('hidden');
}

/**
 * Open a dropdown. This function also automatically sets the active element in the dropdown list.
 * This will only occur if the text in the dropdown title is is contained in the dropdown option that represents it.
 * @param {string} id The ID of the dropdown to open. The dropdown should have that ID in html.
 */
function openDropdown(id) {
	//Get and unhide the element
	let dropdown = document.getElementById(id);
	dropdown.classList.remove('hidden');

	//Get the dropdown title element
	let content = dropdown.getElementsByClassName('dropdown title')[0];

	//Get the text from the dropdown element
	content = content.textContent.trim();

	//Get the dropdown options from the document
	let dropdownOptions = document.getElementById(`${id} content`).children;

	//Go through the list of dropdown options, if any contain the content, make that active and break
	for (let i = 0; i < dropdownOptions.length; i++) {
		//Get the text from the option and convert it to a string
		//Any underscores in the text is treated as a space
		const text = dropdownOptions[i].textContent.toString().replace('_', ' ');

		//If the text contains the title of the dropdown, it is the active item and is selected
		if (text.includes(content)) {
			dropdownOptions[i].classList.add('active');
		} else {
			dropdownOptions[i].classList.remove('active');
		}
	}
}
