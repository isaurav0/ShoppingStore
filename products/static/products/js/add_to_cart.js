function addToCart(id){
	var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	var target = event.target
	let buttonWork = target.getAttribute("data-buttonWork")	

	if(buttonWork=="add"){
        fetch('/products/add_to_cart/'+id, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},	          
          })
			.then(res=>{
				if(res.status === 200){
					target.className = "cart_button added"
					target.setAttribute("data-buttonWork", "remove")
					target.innerHTML = "Already in cart"	
					target.setAttribute("disabled", true)
				}
				if(res.status === 401){
					window.location.href = "/login"
				}
			})
	}

	if(buttonWork=="remove"){
		fetch('/products/remove_from_cart/'+id, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},	          
          })
			.then(res=>{
				if(res.status === 200){
					window.location.reload()		
				}
				if(res.status === 401){
					window.location.href = "/login"
				}
			})
	}
}