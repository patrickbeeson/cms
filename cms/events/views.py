from django.views.generic import DateDetailView, ListView
from django.views.generic.dates import YearMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from cms.events.models import Event, EventType

class EventDetailView(DateDetailView):
	""" View to display an event detail view with the added feature of showing a draft event as live to staff users. """
	date_field = "event_date"
	allow_future = True
	template_name = "events/event_detail.html"
	context_object_name = "event"
	slug_field = "slug"

	def get_queryset(self):
		events = None
		if self.request.user.is_staff:
			events = Event.objects.all()
		else:
			events = Event.live.all()
		return events
	
class VisitingScholarsYearView(YearMixin, ListView):
	""" View to display only Distinguished Visiting Scholar Series events within an academic year for a defined year. """
	allow_empty = True
	template_name = "events/distinguished_visiting_scholars_series_expired.html"
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.academic_year.from_year(self.get_year()).filter(event_type__title='Distinguished Visiting Scholars Series')

	def get_context_data(self, **kwargs):
		context = super(VisitingScholarsYearView, self).get_context_data(**kwargs)
		context['year'] = self.get_year()
		return context

class PublicLecturesListView(ListView):

    context_object_name = "event_list"
    template_name = "events/public-lectures-event_list.html"
    paginate_by = 15

    def get_queryset(self):
        self.event_type = get_object_or_404(EventType, slug__iexact=self.kwargs['slug'])
        return Event.current.filter(event_type=self.event_type).filter(audience_type=1)

    def get_context_data(self, **kwargs):
        context = super(PublicLecturesListView, self).get_context_data(**kwargs)
        context['event_type'] = self.event_type
        return context

class ResearchLecturesListView(ListView):

    context_object_name = "event_list"
    template_name = "events/research-lectures-event_list.html"
    paginate_by = 15

    def get_queryset(self):
        self.event_type = get_object_or_404(EventType, slug__iexact=self.kwargs['slug'])
        return Event.current.filter(event_type=self.event_type).filter(audience_type=2)

    def get_context_data(self, **kwargs):
        context = super(ResearchLecturesListView, self).get_context_data(**kwargs)
        context['event_type'] = self.event_type
        return context

class ExpiredVisitingScholarsSeriesListView(ListView):

	context_object_name = "event_list"
	queryset = Event.expired.filter(event_type__title="Distinguished Visiting Scholars Series")
	template_name = "events/distinguished_visiting_scholars_series_expired.html"
	paginate_by = 15