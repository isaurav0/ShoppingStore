function activateReplyField(){

	target = event.target.parentNode

	
	if(target.getAttribute("data-buttonWork")=="addReplyField"){
		let comment_id = target.getAttribute("data-commentid")
		let comment_field = document.getElementById(comment_id)
		comment_field.style.display = "block"
	}

}	


function addReply(){

	target = event.target

	if(target.getAttribute("role")  =="reply"){

		let comment_id = target.getAttribute("data-commentID")
		let reply_text = target.parentNode.querySelector("input").value

		csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

		if(reply_text.length==0)
			return 

		fetch('/products/comments/'+comment_id+'/comment_reply', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({"reply_text": reply_text}),
          })
		.then(res=>{
			if(res.status == 200){
				
				// set input field to empty again
				target.parentNode.querySelector("input").value = ""
				return res.json()

			}
		})

		.then(res=>{

			//create new Reply Thread

			let newReplyThread = document.getElementById("reply_model").cloneNode(true)

			newReplyThread.querySelectorAll("span.username")[0].innerHTML = document.getElementById("username").innerText

			newReplyThread.querySelectorAll("span.date")[0].innerHTML ='·'+ res['created_at']+'·'

			newReplyThread.querySelectorAll("div.comment_text")[0].innerHTML = res['reply_text'] 

			newReplyThread.style.display = "block"

			//Attach it to the DOM

			target.parentNode.parentNode.querySelector("div.reply_containers").innerHTML += newReplyThread.innerHTML


		})


	}

}