Apr 30 11:29 pm.      
	From my experience in previous project, I have found out that editable div does much better job at taking long paragraph inputs
	than textarea and input tag.  
	Advantages of making editable div over textarea is proper rendering of escape sequence characters in editable field without having to replace `<br>` tag with "\n". To make a div editable, add a property contenteditable to div element like `<div contenteditable>` and that will do it.  
	&nbsp;    		
	We can set div's overflow property to scrollable for better viewing. So, suggestion to myself, 
	choose editable div anyday over textarea and input tags to get rid of headaches.  
	&nbsp;   	
	Another cool stuff I learnt is, when you add float property to child elements of a parent, height of parent 
	collapses. So, adjacent sibling of that parent appear on top of it. Thus overlapping contents.    
	To solve this, we set `clear` property of parent to `both`. And set `display` property to
	`table`. Or another cheap hack can be, 
	adding a child element inside of the parent `<div style="clear: both;"</div>`. And elements added after that will sort 
	out without overlapping.
	&nbsp;   
	&nbsp;   
May 02 2:57 pm.  
	Things can get pretty ugly when creating elements dynamically with javascript. Especially when the element is nested deeply. I can see now why people use frameworks like React.js and Vue.js. At least I learnt the use case of these frameworks and can choose wisely where to use them and where not. I actually feel like crying having to set attributes of children nested deep inside. If I was using react I could have made it a single component and maybe a parent would have a attribute and all of its children would inherit or maybe they wouldn't even need to. Since it was almost impossible to create each elements, I created a model like html element with `display`: `none` that looks somewhat like this. 

```html
	<!-- Comment Model -->
	<div id="comment_model" class="comment_thread" style="display: none;" >

		<!-- comment -->
		<div class="main_comment comment_container">

			<div class="user_info">
				<span class="username"></span>
				<span class="date"></span>
			</div>
			
			<div class="comment_text"></div>	
			<button class="reply_button" data-commentID=""><span><i class="fa fa-comment"></i> Reply</span></button>
		</div>

		<div class="comment_container comment_reply" >
			<div class="reply_containers">
				<!-- Comment Reply Model comes here -->

			</div>

			<!-- in the end is reply button -->
			<div class="comment_row reply_row" id="">	<!-- add id dynamically here comment_id-->
				<input class="comment_textbox" contenteditable placeholder="Add a comment .."></input>
				<submit class="comment_button" role="reply" data-commentID="">Reply</submit>
			</div>
		</div>

	</div>
```  
&nbsp; 
I had to create this element to make it act like a template for creating new elements dynamically. That is a sad thing to do. I have to set innerHTML and attributes of each element using querySelector().  
If I had been using react I would have comment_model a separate tag like <CommentModel> and set all needed attributes like <CommentModel id="comment_model">. And I could reuse its value in all of its child components with ease.  
And if I needed more comment field I could use <CommentMode> tag again anywhere. Vanilla js can get trippy in handling such stuffs. I should definitely use reactjs for such stuffs.  
&nbsp;   
&nbsp;   

May 2 6:36 pm.  
	It is sad to know that keypress events cannot be delegated unlike mouse events. But it makes sense. You have to attach event listeners to every newborn element dynamically created.  
	

