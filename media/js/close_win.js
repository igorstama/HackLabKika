function elem(objId) {
    this.value = document.getElementById(objId)
}

function close_button(objId) {
    this.value = document.getElementById(objId)
}

close_button.prototype.hide = function(el) {
	el.value.style.display = 'none'
}


// Logout window only
window.onload = function() {
	el = new elem('win')
	butt = new close_button('close_button')
	butt.value.onclick = function() {
		butt.hide(el)
	}
}
