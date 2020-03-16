//#region Editing functions
//Generalised functions for edits
function openEdit(editing) {
	//Function is passed string corresponding to the field being edited
	document.getElementById(editing + '-form').style.display = 'block';
	document.getElementById(editing + '-close').style.display = 'block';
	document.getElementById(editing + '-edit').style.display = 'none';
	document.getElementById(editing).style.display = 'none';
}
function closeEdit(editing) {
	//Function is passed string corresponding to the field being edited
	document.getElementById(editing + '-form').style.display = 'none';
	document.getElementById(editing + '-close').style.display = 'none';
	document.getElementById(editing + '-edit').style.display = 'block';
	document.getElementById(editing).style.display = 'block';
}

//Function for changing state between public and private
function setPublic(new_state) {
	console.log(new_state);
}

//Function to delete the product
function deleteProduct(ID) {
	console.log('Delete product with ID: ' + ID);
}
//#endregion

//#region Image slideshow functions
var slideIndex = 0;
slideShow(slideIndex);
//Function to move the slides by the given number
function slideMov(n) {
	slideShow((slideIndex += n));
}

//Function to jump to the given slide number
function slideJmp(n) {
	slideShow((slideIndex = n));
}

//Function to show the current slide
function slideShow(n) {
	var i;
	var slides = document.getElementsByClassName('slide-content');
	var selectors = document.getElementsByClassName('slide-selector overlay');
	if (n < 0) {
		slideIndex = slides.length - 1;
	}
	if (n > slides.length - 1) {
		slideIndex = 0;
	}
	for (i = 0; i <= slides.length - 1; i++) {
		slides[i].style.display = 'none';
	}
	for (i = 0; i <= selectors.length - 1; i++) {
		selectors[i].style.display = 'block';
	}
	slides[slideIndex].style.display = 'flex';
	selectors[slideIndex].style.display = 'none';
}
//#endregion
