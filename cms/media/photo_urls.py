from django.conf.urls.defaults import patterns, include, url
from cms.media.models import Photo
from django.views.generic import ListView, YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView, DateDetailView
from cms.media.views import PhotoDetailView

urlpatterns = patterns('',
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', PhotoDetailView.as_view()),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view(
		queryset = Photo.live.all(),
		date_field = "uploaded",
		template_name = "media/photo_archive_day.html",
		context_object_name = "photo_list",		
	)),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view(
		queryset = Photo.live.all(),
		date_field = "uploaded",
		template_name = "media/photo_archive_month.html",
		context_object_name = "photo_list",	
	)),
	(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
		queryset = Photo.live.all(),
		date_field = "uploaded",
		template_name = "media/photo_archive_year.html",
		context_object_name = "photo_list",
		make_object_list = True,
	)),
	(r'^$', ListView.as_view(
		queryset = Photo.live.all().order_by('-uploaded'),
		template_name = "media/photo_list.html",
		context_object_name = "photo_list",
		paginate_by = 15,
	)),

)