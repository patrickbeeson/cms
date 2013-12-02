from django.conf.urls.defaults import patterns, include, url
from cms.news.models import Story
from django.views.generic import ListView, YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView, DateDetailView
from cms.news.views import StoryDetailView

urlpatterns = patterns('',
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', StoryDetailView.as_view()),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view(
		queryset = Story.live.all(),
		date_field = "pub_date",
		template_name = "news/story_archive_day.html",
		context_object_name = "story_list",		
	)),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view(
		queryset = Story.live.all(),
		date_field = "pub_date",
		template_name = "news/story_archive_month.html",
		context_object_name = "story_list",	
	)),
	(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
		queryset = Story.live.all(),
		date_field = "pub_date",
		template_name = "news/story_archive_year.html",
		context_object_name = "story_list",
		make_object_list = True,
	)),
	(r'^$', ListView.as_view(
		queryset = Story.live.all().order_by('-pub_date'),
		template_name = "news/story_list.html",
		context_object_name = "story_list",
		paginate_by = 15,
	)),
)