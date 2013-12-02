from django.db import models
from django.contrib.localflavor.us.models import *
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google

from cms.places.models import Place
from cms.media.models import Video
from cms.categories.models import Category

import datetime

import tagging
from tagging.fields import TagField

class EventType(Category):

	def __unicode__(self):
		return self.title
	
	def get_absolute_url(self):
		return "/events/%s/" % (self.slug)

	def current_event_set(self):
		""" Returns current events for an event type. """
		return self.event_set.filter(event_date__gte=datetime.date.today()).filter(status=3)

	def live_event_set(self):
		""" Returns live events for an event type. """
		return self.event_set.filter(status=3)

	def academic_event_set(self):
		""" Returns live events within the current academic year for an event type. """
		now = datetime.datetime.now()
		current_year = now.year
		start_date = datetime.date(current_year, 7, 1)
		end_date = datetime.date((current_year + 1), 6, 30)
		return self.event_set.filter(status=3).filter(event_date__range=(start_date, end_date))

class CurrentManager(models.Manager):
	def get_query_set(self):
		return super(CurrentManager, self).get_query_set().filter(event_date__gte=datetime.date.today()).filter(status=self.model.LIVE_STATUS)

class LiveEventManager(models.Manager):
	def get_query_set(self):
		return super(LiveEventManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class ExpiredEventManager(models.Manager):
	def get_query_set(self):
		return super(ExpiredEventManager, self).get_query_set().filter(event_date__lte=datetime.date.today()).filter(status=self.model.LIVE_STATUS)

class AcademicYearManager(models.Manager):
	def live_events(self, start_date, end_date):
		return self.filter(status=self.model.LIVE_STATUS).filter(event_date__range=(start_date, end_date))

	def this_year(self):
		now = datetime.datetime.now()
		current_year = now.year
		start_date = datetime.date(current_year, 7, 1)
		end_date = datetime.date((current_year + 1), 6, 30)
		return self.live_events(start_date, end_date)

	def from_year(self, year):
		start_date = datetime.date(int(year), 7, 1)
		end_date = datetime.date((int(year) + 1), 6, 30)
		return self.live_events(start_date, end_date)

class Event(models.Model):
	GENERAL_PUBLIC = 1
	ACADEMIC = 2
	AUDIENCE_CHOICES = (
		(GENERAL_PUBLIC, 'Public'),
		(ACADEMIC, 'Research'),
	)
	LIVE_STATUS = 3
	DRAFT_STATUS = 4
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
	)
	pub_date = models.DateTimeField(default=datetime.datetime.now, editable=False, auto_now_add=True)
	
	slug = models.SlugField(unique_for_date='pub_date', help_text="This field will prepopulate from the name field.")
	name = models.CharField(max_length=200, help_text="Limited to 200 characters.")
	
	host = models.ForeignKey(User, blank=True, null=True)
	one_off_host = models.CharField(max_length=100, help_text="Limited to 100 characters.", blank=True)
	contact_email = models.EmailField(blank=True)
	contact_phone_number = PhoneNumberField(blank=True, null=True)
	external_URL = models.URLField(blank=True, help_text="The URL of the website containing additional information.")
	
	speaker = models.CharField(max_length=200, help_text="Limited to 200 characters.", blank=True)
	speaker_title = models.CharField(max_length=250, help_text="Limited to 250 characters.", blank=True)
	speaker_bio = models.TextField(blank=True, help_text='No HTML is allowed.')
	speaker_website = models.URLField(blank=True)
	speaker_mugshot = models.ImageField(upload_to='images/events/speaker_mugshots', blank=True)
	
	room_or_area = models.CharField(max_length=250, help_text="Limited to 250 characters.", blank=True)
	audience_type = models.IntegerField(choices=AUDIENCE_CHOICES, default=2)
	is_free = models.BooleanField(default=True)
	cost = models.IntegerField(blank=True, null=True, help_text="No dollar sign is required.")
	notes = models.TextField(blank=True, help_text="Any additional information that might be helpful to attendees. Examples include: receptions, special dress, etc.")
	has_webcast = models.BooleanField(default=False, help_text="Check this box to indicate whether or not the event will be broadcast on the web.")
	
	location = models.ForeignKey(Place, null=True, on_delete=models.SET_NULL)
	
	description = models.TextField(help_text='A brief description of the event. No HTML is allowed.', blank=True)

	status = models.IntegerField(choices=STATUS_CHOICES, default=4, help_text="Only events with a status of 'live' will be displayed publicly.")
	
	event_date = models.DateField()
	start_time = models.TimeField(blank=True, null=True)
	finish_time = models.TimeField(blank=True, null=True)
	is_all_day_event = models.NullBooleanField(blank=True, null=True, default=False, help_text='Indicate whether the event lasts the entire day. Please leave the start time and finish time fields blank if the event lasts all day.')
	tags = TagField(help_text="Separate tags with spaces.")
	event_type = models.ManyToManyField(EventType)

	lead_image = models.ImageField(upload_to='images/events', blank=True)
	archived_webcast = models.ForeignKey(Video, null=True, blank=True, on_delete=models.SET_NULL)
	
	sites = models.ManyToManyField(Site)
	
	objects = models.Manager()
	current = CurrentManager()
	live = LiveEventManager()
	expired = ExpiredEventManager()
	academic_year = AcademicYearManager()

	class Meta:
		ordering = ['-event_date']
		verbose_name_plural = 'events'
	
	def __unicode__(self):
		return self.name

	def save(self, force_insert=False, force_update=False):
		super(Event, self).save(force_insert, force_update)
		try:
			ping_google()
		except Exception:
			pass

	def get_absolute_url(self):
		return "/events/%s/%s/" % (self.event_date.strftime("%Y/%b/%d").lower(), self.slug)

	@property		
	def is_expired(self):
		"""Returns True if the event's date is less than the current date."""
		return self.event_date < datetime.date.today()

	@property
	def show_webcast(self):
		from datetime import date, datetime, time, timedelta
		"""Returns True the current time is 15 minutes before the start time and an hour after the finish time."""
		st = datetime.combine(self.event_date, self.start_time) - timedelta(minutes=15)
		ft = datetime.combine(self.event_date, self.finish_time) + timedelta(minutes=60)
		ct = datetime.now()
		if self.is_expired:
			return False
		elif self.has_webcast == False:
			return False
		else:
			while (ct > st):
				if ct > ft:
					break
				return True

	def show_archived_webcast(self):
		if self.archived_webcast and self.archived_webcast.is_expired == False:
			return True
		else:
			return False

	@property
	def related_event_set(self):
		eventtype_id_list = self.event_type.values_list("id", flat=True)
		return Event.current.filter(event_type__id__in=eventtype_id_list).exclude(id=self.id).distinct()[:5]