function addComment(){
	
	var target = event.target
		
	if(target.getAttribute("data-buttonWork")=="comment"){

		var post_id = target.getAttribute("data-postID")
	
		var parent = event.target.parentNode

		var comment_text_container = parent.querySelector("input#comment_text")
		comment_text = comment_text_container.value
		console.log(comment_text)

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