from django.conf.urls.defaults import patterns, include, url
from cms.media.models import Audio
from django.views.generic import ListView, DetailView
from cms.media.views import AudioDetailView

urlpatterns = patterns('',
	(r'^$', ListView.as_view(
		queryset = Audio.live.all().order_by('-uploaded'),
		template_name = "media/audio_list.html",
		context_object_name = "audio_list",
		paginate_by = 15,
	)),
	
	(r'^(?P<slug>[-\w]+)/$', AudioDetailView.as_view()),

)