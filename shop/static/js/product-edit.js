//The functions in this file are not currently in active use, but may be used for product editing later
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
