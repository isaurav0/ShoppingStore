function addToCart(id){
	var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	let buttonWork = event.target.getAttribute("data-buttonWork")
	var target = event.target

	if(buttonWork=="add"){
        fetch('/products/add_to_cart/'+id, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},	          
          })
			.then(res=>{
				if(res.status == 200){
					target.className = "cart_button added"
					target.setAttribute("data-buttonWork", "remove")
					target.innerHTML = "Remove From Cart"
				}
				return res.json()						
			})				
	}

	else{
		
		fetch('/products/remove_from_cart/'+id, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},	          
          })
			.then(res=>{
				if(res.status == 200){
					target.className = "cart_button"	
					target.setAttribute("data-buttonWork", "add")	
					target.innerHTML = "Add To Cart"					
				}
				return res.json()						
			})
			.then(res=>{
				return 
			})
	}
}