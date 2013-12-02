from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.contrib.sitemaps import ping_google

from markdown import markdown
import datetime

from tagging.fields import TagField

import tagging
from cms.categories.models import Category
from cms.related_links.models import RelatedLink
from cms.media.models import Photo, Video, Gallery, Audio
from cms.events.models import Event
from cms.static_media.models import Document
from cms.employees.models import Employee, Publication
from cms.places.models import City

class LiveStoryManager(models.Manager):
	def get_query_set(self):
		return super(LiveStoryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Story(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
	)
	slug = models.SlugField(unique_for_date='pub_date', help_text="This field will automatically populate from the headline.")
	headline = models.CharField(max_length=250, help_text="Limited to 250 characters.")
	subhead = models.CharField(max_length=250, help_text="Limited to 250 characters.", blank=True)

	summary = models.TextField(help_text="A brief description of what this story is about.")
	body = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a> for all text-formatting and links. No HTML is allowed.')
	body_html = models.TextField(blank=True, editable=False)
	
	tease_photo = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL, related_name="tease_photo", help_text="Used for teasing to the story only, such as on the homepage. Will not be displayed on the story itself.")
	photo = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL, related_name="lead_photo", limit_choices_to={'status__in': [1]})

	related_videos = models.ManyToManyField(Video, blank=True, limit_choices_to={'status__lte': 1})
	related_events = models.ManyToManyField(Event, blank=True, limit_choices_to={'event_date__gte': datetime.date.today()})
	related_galleries = models.ManyToManyField(Gallery, blank=True, limit_choices_to={'status__lte': 1})
	related_audio = models.ManyToManyField(Audio, blank=True, limit_choices_to={'status__lte': 1})
	related_documents = models.ManyToManyField(Document, blank=True)
	related_links = generic.GenericRelation(RelatedLink, blank=True)
	related_publications = models.ManyToManyField(Publication, blank=True)
	related_photos = models.ManyToManyField(Photo, blank=True, related_name='related_photos', limit_choices_to={'status__lte': 1})

	pub_date = models.DateTimeField(default=datetime.datetime.now)
	updated = models.DateTimeField(blank=True, null=True)

	author = models.ForeignKey(User, limit_choices_to={'groups__name__exact': 'Writers'}, blank=True, null=True)
	one_off_byline = models.CharField(max_length=200, blank=True, help_text='Format: Person Name, person@email.edu')

	media_contact = models.ForeignKey(User, related_name='media_contact', limit_choices_to={'groups__name__exact': 'Communicators'}, blank=True, null=True)
	one_off_media_contact = models.CharField(max_length=200, blank=True, null=True, help_text='Format: Person Name, person@email.edu')

	status = models.IntegerField(choices=STATUS_CHOICES, default=2, help_text="Only stories with a status of 'live' will be displayed publicly.")
	dateline = models.ForeignKey(City)
	faculty_profiled = models.ManyToManyField(Employee, related_name="stories_for_subject", help_text="Choose the faculty members who this story mentions or profiles. Used to build list of related stories for each faculty member.", blank=True)
	
	categories = models.ManyToManyField(Category, limit_choices_to={'topic__category_ptr__isnull': True, 'eventtype__category_ptr__isnull': True})
	tags = TagField(help_text="Separate tags with spaces.")
	sites = models.ManyToManyField(Site)

	objects = models.Manager()
	live = LiveStoryManager()

	class Meta:
		ordering = ['-pub_date']
		verbose_name = "story"
		verbose_name_plural = "stories"
		
	def __unicode__(self):
		return self.headline

	def get_absolute_url(self):
		return '/news/%s/%s/' % (self.pub_date.strftime('%Y/%b/%d').lower(), self.slug)

	def get_categories_with_stories(self):
		categories = self.category.all()
		for category in categories:
			category.stories = category.story_set.exclude(id=self.id)[:5]
		return categories

	@property
	def related_story_set(self):
		category_id_list = self.categories.values_list("id", flat=True)
		return Story.live.filter(categories__id__in=category_id_list).exclude(id=self.id).distinct()[:5]			

	def save(self, force_insert=False, force_update=False):
		self.body_html = markdown(self.body)
		super(Story, self).save(force_insert, force_update)
		try:
			ping_google()
		except Exception:
			pass

	def live_audio_set(self):
		""" Returns live audio for a story """
		return self.related_audio.all().filter(status=1)

	def live_photo_set(self):
		""" Returns live photos for a story """
		return self.related_photos.all().filter(status=1)

	def live_gallery_set(self):
		""" Returns live galleries for a story """
		return self.related_galleries.all().filter(status=1)

	def live_video_set(self):
		""" Returns live videos for a story """
		return self.related_videos.all().filter(status=1)
		
	def active_faculty_set(self):
		""" Returns active faculty for a story """
		return self.faculty.filter(is_currently_employed=True)

	def current_event_set(self):
		""" Returns current events for a news story """
		return self.related_events.all().filter(status=1)