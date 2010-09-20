function counter(val) {
        this.value = val;
}
counter.prototype.subtract = function() {
        this.value -= 100;
}

function elem(objId) {
        this.value = document.getElementById(objId)
}

elem.prototype.getChildrenByTagName = function(nodeName) {
	elements = new Array()
	nodeName = nodeName.toLowerCase()
	c = 0
	for (i = 0; i < this.value.childNodes.length; i++) { 
		if (this.value.childNodes[i].nodeName.toLowerCase() == nodeName) { 
			elements[c] = this.value.childNodes[i]
			c++
		}
	}
	return elements
}

elem.prototype.clearNodes = function() {
	this.value.innerHTML = ""
}
elem.prototype.addNode = function(node) {
	this.value.appendChild(node)
	node.style.right = -(node.innerText.length*3) + "px"
}
elem.prototype.move = function(pos) {
	this.value.style.marginRight = pos + "px"
}

function scroll_one(el, interval, timer, news) {
	if (timer.value < 1){
		clearInterval(interval)
		// ova e proba za rekurzivno povikuvanje na 
		// glavnata funkcija za skrolanje
		scroll_all(news)
	}
	else if(timer.value > 1) {
		if (!el.style.right)
			el.style.right = -el.innerText.length*3 + "px"
		el.style.right = parseInt(el.style.right.substring(0, el.style.right.length-2)) + 1 + "px"
        timer.subtract()
    }    
}

function scroll_all(news, el) {
	el.clearNodes()
	text = news.shift()
	el.addNode(text)
	if (text != undefined) {
		timer = new counter(text.innerText.length * 1000)
		interval = setInterval("scroll_one(text, interval, timer, news)", 15)
	}
}

// Logout window only
window.onload = function() {
        el = new elem('scroller')
		news = el.getChildrenByTagName("p")
		
		// el.clearNodes()
        // scroll_all(news, el)
}
