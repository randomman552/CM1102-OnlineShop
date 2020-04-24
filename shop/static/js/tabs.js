/**
 * This function switches between two tabs (when they are defined like the one on the products page).
 * Elements to switch between should have the class "tab" (so they can be fetched).
 * The buttons that call this function should have an ID of "{tabName} button", 
 * and a class name of tab-button.
 * The buttons will have a .active class added to them when the tab switches to that tab.
 * The tabs should have ids of "{tabname} tab"
 * When one of the buttons is 
 * @param {string} newTab 
 */
function switchTab(newTab) {
	//Get all the tabs in the document, and the one we are switching to
	let allTabs = document.getElementsByClassName('tab');
	let toSwitchTo = document.getElementById(`${newTab} tab`);

	//Get the buttons for this operation
	let allButtons = document.getElementsByClassName('tab-button');
	let newButton = document.getElementById(`${newTab} button`);

	//Make sure the tab to switch to actually exists
	if (toSwitchTo != null) {
		//Give hidden class name to all tabs
		for (let i = 0; i < allTabs.length; i++) {
			const element = allTabs[i];
			element.classList.add('hidden');
		}

		//Remove the active class name from all buttons
		for (let i = 0; i < allButtons.length; i++) {
			const element = allButtons[i];
			element.classList.remove('active');
		}

		//Remove the hidden class from the tab we are switching to
		toSwitchTo.classList.remove('hidden');

		//If the button is not null, make it active
		if (newButton != null) {
			newButton.classList.add('active');
		}
	}
}
