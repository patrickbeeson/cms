from django.conf.urls.defaults import patterns, include, url
from cms.media.models import Video
from django.views.generic import ListView, YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView, DateDetailView
from cms.media.views import VideoDetailView

urlpatterns = patterns('',
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', VideoDetailView.as_view()),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view(
		queryset = Video.live.all(),
		date_field = "created",
		template_name = "media/video_archive_day.html",
		context_object_name = "video_list",		
	)),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view(
		queryset = Video.live.all(),
		date_field = "created",
		template_name = "media/video_archive_month.html",
		context_object_name = "video_list",	
	)),
	(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
		queryset = Video.live.all(),
		date_field = "created",
		template_name = "media/video_archive_year.html",
		context_object_name = "video_list",
		make_object_list = True,
	)),
	(r'^$', ListView.as_view(
		queryset = Video.live.all().order_by('-created'),
		template_name = "media/video_list.html",
		context_object_name = "video_list",
		paginate_by = 15,
	)),

)