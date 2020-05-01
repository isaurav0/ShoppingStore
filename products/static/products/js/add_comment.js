function addComment(){
	
	const target = event.target
		
	if(target.getAttribute("data-buttonWork")=="comment"){

		const post_id = target.getAttribute("data-postID")
	
		const parent = event.target.parentNode

		const comment_text_container = parent.querySelector("input#comment_text")
		const comment_text = comment_text_container.value

		//should go in 
		let newCommentThread = document.getElementById("comment_model").cloneNode(true)
		console.log(newCommentThread)


		// above 
		if(comment_text.length == 0 )
			return 

        csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;			


		fetch('/products/'+post_id+'/add_comment', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({"comment_text": comment_text}),
          })
		.then(res=>{
			if(res.status == 200){
				console.log("success")
				comment_text_container.value = ""				

			}

		})
	}

	return 

}