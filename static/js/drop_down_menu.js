// Drop-down menu

$(document).ready(function(){
	$(".submenu").hide(); // Hide the submenu by default
	$(".dropdown").append('<span class="arrow"></span>'); // Add span hook for CSS arrow
	$(".dropdown").hover(function() {
		$(this).find(".submenu").show();
		$(this).addClass("selected");
	},
	function () {
		$(this).find(".submenu").hide();
		$(this).removeClass("selected");
	});
});