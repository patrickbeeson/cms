from django import template

import datetime

from cms.events.models import Event, EventType

def do_upcoming_livewebcast_events(parser, token):
	"""
	Gets a list of all upcoming events with a live webcast.
	
	Syntax::
	
		{% get_upcoming_livewebcast_events %}
	
	Example::
	
		{% get_upcoming_livewebcast_events %}
		<ul>
		{% for event in upcoming_livewebcast_events %}
			<li>{{ event.name }}</li>
		{% endfor %}
		</ul>
	"""
	return UpcomingLivewebcastEventsNode()

class UpcomingLivewebcastEventsNode(template.Node):
	def render(self, context):
		context['upcoming_livewebcast_events'] = Event.current.all().filter(has_webcast=True).order_by('event_date')
		return ''

def do_expired_events_for_eventtype(parser, token):
	"""
	Gets a list of all expired events for an eventtype, and passes it into a custom variable.
	
	Syntax::
	
		{% get_expired_events_for_eventtype [eventtype] as [varname] %}
	
	Example::
	
		{% get_expired_events_for_eventtype lectures as lectures_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 4:
		raise template.TemplateSyntaxError("'get_expired_events_for_eventtype' tag takes exactly three arguements.")
	return Expired_EventsForEventTypeNode(bits[1], bits[3])
	
class Expired_EventsForEventTypeNode(template.Node):
	def __init__(self, eventtype, varname):
		self.eventtype = eventtype
		self.varname = varname
		
	def render(self, context):
                try:
                    et = EventType.objects.get(slug=self.eventtype)
		    context[self.varname] = et.event_set.all().filter(event_date__lte=datetime.date.today()).order_by('-event_date')
                except EventType.DoesNotExist:
                    pass
		return ''

def do_upcoming_events_for_eventtype(parser, token):
	"""
	Gets a list of n number of upcoming events for an eventtype, and passes it into a custom variable.
	
	Syntax::
	
		{% get_upcoming_events_for_eventtype [eventtype] [number] as [varname] %}
	
	Example::
	
		{% get_upcoming_events_for_eventtype lectures 5 as lectures_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 5:
		raise template.TemplateSyntaxError("'get_upcoming_events_for_eventtype' tag takes exactly four arguements.")
	return UpcomingEventsForEventTypeNode(bits[1], bits[2], bits[4])
	
class UpcomingEventsForEventTypeNode(template.Node):
	def __init__(self, eventtype, num, varname):
		self.eventtype = eventtype
		self.num = int(num)
		self.varname = varname
		
	def render(self, context):
                try:
                    et = EventType.objects.get(slug=self.eventtype)
		    context[self.varname] = et.event_set.all().filter(event_date__gte=datetime.date.today()).order_by('event_date')[:self.num]
                except EventType.DoesNotExist:
                    pass
		return ''

register = template.Library()
register.tag('get_upcoming_livewebcast_events', do_upcoming_livewebcast_events)
register.tag('get_expired_events_for_eventtype', do_expired_events_for_eventtype)
register.tag('get_upcoming_events_for_eventtype', do_upcoming_events_for_eventtype)