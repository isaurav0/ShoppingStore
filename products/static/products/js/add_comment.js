function addComment(){
	
	const target = event.target
		
	if(target.getAttribute("data-buttonWork")=="comment"){

		const post_id = target.getAttribute("data-postID")
	
		//to get input value
		const parent = event.target.parentNode	
		const comment_text_container = parent.querySelector("input.comment_textbox")
		const comment_text = comment_text_container.value

		if(comment_text.length == 0 )
			return 

        csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;			

        //send request to server
		fetch('/products/'+post_id+'/add_comment', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({"comment_text": comment_text}),
          })
		.then(res=>{
			if(res.status == 200){
				console.log("success")
				comment_text_container.value = ""
				return res.json()
			}

		})
		.then(res =>{
			//create New Comment Thread
			let newCommentThread = document.getElementById("comment_model").cloneNode(true)		
		
			newCommentThread.querySelectorAll("span.username")[0].innerText = document.getElementById("username").innerText

			newCommentThread.querySelectorAll("span.date")[0].innerText = '· '+res['created_at']+' ·'

			newCommentThread.querySelectorAll("div.comment_text")[0].innerText = res['comment_text']

			newCommentThread.querySelectorAll("button.reply_button")[0].setAttribute("data-commentID", res['comment_id'])

			newCommentThread.querySelectorAll("div.comment_row.reply_row")[0].id = res['comment_id']

			newCommentThread.querySelectorAll("submit.comment_button")[0].setAttribute("data-commentID", res['comment_id'])

			newCommentThread.style.display = "block"
			newCommentThread.removeAttribute("id")

			//attach it to DOM
			var previous_comments_block = document.getElementById("previous_comments")
			previous_comments_block.insertBefore(newCommentThread, previous_comments_block.childNodes[0])
		})
	}

	return 
}


// Comment on hitting Enter button 
var comment_boxes =  document.querySelectorAll("input.comment_textbox")

comment_boxes.forEach(box=>{
	box.addEventListener("keyup", listenEnter)
})

function listenEnter(event){
	if(event.keyCode === 13){
		event.target.parentNode.querySelector("submit.comment_button").click();
	}
}
