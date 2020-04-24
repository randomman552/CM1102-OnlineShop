//This document contains the code needed for the slideshow on the view product page

//Setup slideshow
var slideTime = 5000;
var slideIndex = 0;
slideShow(slideIndex);
var slideIntervalID = 0;
slideShowResume();
slideShowControlsState(false);

/**
 * Move the slide by the given number of slides. 
 * This also interupts the slideshow timer.
 * @param {number} n The number of slides to move by (can be negative or positive)
 */

function slideMov(n) {
	slideShowPause();
	slideShowResume();
	slideShow((slideIndex += n));
}

/**
 * Jump to a slide position
 * @param {number} n The position to jump to
 */
function slideJmp(n) {
	slideShowPause();
	slideShowResume();
	slideShow((slideIndex = n));
}

/**
 * Update the slide to the given position
 * This should not be called directly, but is called by slideJmp and slideMov
 * @param {number} n The slide number to make active (all others are inactive)
 */
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
		selectors[i].classList.remove('active');
	}
	slides[slideIndex].style.display = 'flex';
	selectors[slideIndex].classList.add('active');
}

/**
 * Pause the slideshow.
 */
function slideShowPause() {
	clearInterval(slideIntervalID);
}

/** Resume the slideshow */
function slideShowResume() {
	slideIntervalID = setInterval(function() {
		slideMov(1);
	}, slideTime);
}

/**
 * Set the state of the slide show controls.
 * This will hide the elements with the id 'slideshow-prev' or 'slideshow-next'
 * @param {boolean} state If true, the slide show controls will become visible, 
 * otherwise they will become invisibile
 */
function slideShowControlsState(state) {
	var controls = [ document.getElementById('slideshow-prev'), document.getElementById('slideshow-next') ];
	if (state == false) {
		controls.forEach((element) => {
			element.classList.add('hidden');
		});
	} else {
		controls.forEach((element) => {
			element.classList.remove('hidden');
		});
	}
}
