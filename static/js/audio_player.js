$(document).ready(function() {
	var ua = $.browser;
	if (ua.mozilla) {
		$('.content_body').find('audio').hide();
		$('<a href="{{ STATIC_URL }}{{ audio.audio }}">Download the audio</a>').insertBefore('#byline');
	};
}); 