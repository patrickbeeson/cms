// Gallery Script

$(document).ready(function(){
	$('<div id="lead_photo"></div>').insertBefore("#image_gallery"); // Build the container for the main image
	$('#lead_photo').append('<img id="current_image">'); // Put the img inside the div
	var first_img_src = $('#image_gallery').find('a').first().clone().attr('href');
	//var first_img_title = $('#image_gallery').find('.title').first().clone().contents();
	var first_img_photographer = $('#image_gallery').find('.photographer').first().clone().contents();
	var first_img_caption = $('#image_gallery').find('.caption').first().clone().contents();
	$('#current_image').attr('src', first_img_src);
	//$('#lead_photo').append('<h2 id="lead_photo_title"></h2>'); // Add h2 for img title
	//$('#lead_photo_title').append(first_img_title);
	$('#lead_photo').append('<p id="lead_photo_photographer"></p>'); // Add div to contain img photographer
	$('#lead_photo_photographer').append(first_img_photographer);
	$('#lead_photo').append('<div id="lead_photo_caption"></div>'); // Add div to contain img caption
	$('#lead_photo_caption').append(first_img_caption);
	$('#image_gallery .caption').addClass('hidden'); // Hide thumbnail caption
	$('#image_gallery .title').addClass('hidden'); // Hide thumbnail title
	$('#image_gallery .photographer').addClass('hidden'); // Hide thumbnail title
	$("#image_gallery li a").click(function(event) { // Action happens when the linked thumbnail is clicked
		var img_src = $(this).attr("href"); // Set main image src from the link's src (large image)
		var img_alttext = $(this).children().attr("alt"); // Set main image alt from the current thumbnail alt
		//var img_title = $(this).next().clone().contents(); // Set main image title from thumbnail title
		var img_photographer = $(this).next().next().clone().contents(); // Set main image photographer from thumbnail photographer
		var img_caption = $(this).next().next().next().clone().contents(); // Set main image caption from thumbnail caption
		$('#current_image').attr('alt', img_alttext); // Insert alt
		$('#current_image').attr('src', img_src); // Insert src
		//$('#lead_photo_title').empty().append(img_title); // Insert the title
		$('#lead_photo_photographer').empty().append(img_photographer); // Insert photographer
		$('#lead_photo_caption').empty().append(img_caption); // Insert caption
		event.preventDefault(); // Prevent users from following link to full image
	});
});