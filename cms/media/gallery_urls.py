from django.conf.urls.defaults import patterns, include, url
from cms.media.models import Gallery
from django.views.generic import ListView, YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView, DateDetailView
from cms.media.views import GalleryDetailView

urlpatterns = patterns('',
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', GalleryDetailView.as_view()),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view(
		queryset = Gallery.live.all(),
		date_field = "created",
		template_name = "media/gallery_archive_day.html",
		context_object_name = "gallery_list",		
	)),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view(
		queryset = Gallery.live.all(),
		date_field = "created",
		template_name = "media/gallery_archive_month.html",
		context_object_name = "gallery_list",	
	)),
	(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
		queryset = Gallery.live.all(),
		date_field = "created",
		template_name = "media/gallery_archive_year.html",
		context_object_name = "gallery_list",
		make_object_list = True,
	)),
	(r'^$', ListView.as_view(
		queryset = Gallery.live.all().order_by('-created'),
		template_name = "media/gallery_list.html",
		context_object_name = "gallery_list",
		paginate_by = 15,
	)),

)