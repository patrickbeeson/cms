from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView, YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView, DateDetailView

from cms.events.models import Event, EventType
from cms.events.views import EventDetailView, VisitingScholarsYearView

urlpatterns = patterns('',
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', EventDetailView.as_view()),

	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view(
		allow_future = True,
		queryset = Event.current.all().order_by('event_date'),
		date_field = "event_date",
		template_name = "events/event_archive_day.html",
		context_object_name = "event_list",		
	)),
	
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view(
		allow_future = True,
		queryset = Event.current.all().order_by('event_date'),
		date_field = "event_date",
		template_name = "events/event_archive_month.html",
		context_object_name = "event_list",	
	)),
	
	url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
		allow_future = True,
		queryset = Event.current.all().order_by('event_date'),
		date_field = "event_date",
		template_name = "events/event_archive_year.html",
		context_object_name = "event_list",
		make_object_list = True,
	)),
	
	url(r'^$', ListView.as_view(
		template_name = "events/event_list.html",
		context_object_name = "event_list",
		paginate_by = 15,
		queryset = Event.current.all().order_by('event_date'),
	)),
	
	url(r'^(?P<slug>[-\w]+)/public-lectures/$', PublicLecturesListView.as_view()),
	
	url(r'^(?P<slug>[-\w]+)/research-seminars/$', ResearchSeminarsListView.as_view()),
    
    url(r'^(?P<slug>[-\w]+)/$', DetailView.as_view(
    	context_object_name = "eventtype",
    	template_name_field = "template_name",
    	model = EventType,
    )),

    url(r'^distinguished-visiting-scholars-series/(?P<year>\d{4})/$', VisitingScholarsYearView.as_view()),
	
	url(r'^distinguished-visiting-scholars-series/expired/$', ExpiredVisitingScholarsSeriesListView.as_view()),
)