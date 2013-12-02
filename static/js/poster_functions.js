$(document).ready(function(){
	$('#news_posters').carousel('#poster_previous', '#poster_next');  
	
	//The auto-scrolling function
	function slide(){
		$('#poster_next').click();
	}
	
	//Launch the scroll every 4 seconds
	var intervalId = window.setInterval(slide, 4000);

	//If user hovers over the poster area, deactivate auto-scrolling
	$('#news_posters').hover(
		function(event){
			if(event.originalEvent){
				window.clearInterval(intervalId);
			}
		}
	);
});