from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from cms.events.models import Event, EventType

current_site = Site.objects.get_current()

class UpcomingEvents(Feed):
	description_template = 'feeds/events_description.html'
	title_template = 'feeds/events_title.html'
	title = "Upcoming events | %s" % current_site.name
	link = "http://somedomain.com/events/"
	description = "Upcoming events..."

	def items(self):
		return Event.current.order_by('-event_date')[:10]
		
	def item_title(self, item):
		return item.name
		
	def item_description(self, item):
		return item.description

class UpcomingEventsByEventType(Feed):
	description_template = 'feeds/eventtypes_description.html'
	title_template = 'feeds/eventypes_title.html'
	
	def get_object(self, request, slug):
		return get_object_or_404(EventType, slug=slug)
		
	def title(self, obj):
		return "Upcoming events for %s event type | %s" % (obj.title, current_site.name)
	
	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return obj.get_absolute_url()
	
	def description(self, obj):
		return "%s" % obj.description

	def items(self, obj):
		return Event.current.filter(event_type__slug__exact=obj.slug).order_by('-event_date')[:10]