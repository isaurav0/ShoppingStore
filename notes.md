Apr 30 11:29pm
	From my experience in previous project, I have found out that editable div does much better job at taking long paragraph inputs
	than textarea and input tag. Advantages of making editable div over textarea is proper rendering of escape
	sequence characters in editable field without having to replace <br> tag with "\n". To make a div editable, add a property 
	contenteditable to div element. 

	<div contenteditable> and that will do it.

	We can set div's overflow property to scrollable for better viewing. So, suggestion to myself, 
	choose editable div anyday over textarea and input tags to get rid of headaches.

	
	Another cool stuff I learnt is, when you add float property to child elements of a parent, height of parent 
	collapses. So, adjacent sibling of that parent appear on top of it. Thus overlapping contents. To solve this, 
	we set `clear` property of parent to `both`. And set `display` property to `table`. Or another cheap hack can be, 
	adding a child element inside of the parent <div style="clear: both;"</div> And elements added after that will sort 
	out without overlapping.