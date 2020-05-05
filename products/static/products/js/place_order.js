function placeOrder(){

	var fullname = document.getElementById("fullname").value
	var address = document.getElementById("address").value

	var carts = document.getElementsByClassName("items")
	var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	// console.log(carts)

	var carts_data = []

	for(i=0; i<carts.length; i++){
		cart_data = {}
		id = carts[i].id
		title = carts[i].querySelectorAll("div.item_title")[0].innerText

		category = carts[i].querySelectorAll("span.category")[0].innerText
		type = carts[i].querySelectorAll("span.type")[0].innerText
		quantity = carts[i].querySelectorAll("input.quantity")[0].value

		cart_data = {id, title, category, type, quantity}
		carts_data.push(cart_data)
	}

	var data = { "products": carts_data, "address": address, "fullname": fullname }



	fetch('/products/place_order', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify(data)
          })
			.then(res=>{
				if(res.status === 200){
					document.getElementById("page").style.display = "none"
					document.getElementById("success").style.display = "block"
				}
			})
			.then(res=>{
				console.log(res)
			})
}