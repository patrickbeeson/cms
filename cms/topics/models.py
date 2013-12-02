from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic

from cms.news.models import Story
from cms.media.models import Audio, Photo, Gallery, Video
from cms.employees.models import Employee
from cms.static_media.models import Document
from cms.related_links.models import RelatedLink
from cms.categories.models import Category

class Topic(Category):
	stories = models.ManyToManyField(Story, blank=True, limit_choices_to={'status__lte': 1})
	photos = models.ManyToManyField(Photo, blank=True, limit_choices_to={'status__lte': 1})
	galleries = models.ManyToManyField(Gallery, blank=True, limit_choices_to={'status__lte': 1})
	videos = models.ManyToManyField(Video, blank=True, limit_choices_to={'status__lte': 1})
	audio = models.ManyToManyField(Audio, blank=True, limit_choices_to={'status__lte': 1})
	documents = models.ManyToManyField(Document, blank=True)
	faculty = models.ManyToManyField(Employee, blank=True, limit_choices_to={'is_currently_employed__exact': True})
	related_links = generic.GenericRelation(RelatedLink, blank=True)
	is_expired = models.BooleanField(default=False, help_text='Check this box to remove this topic from the public.')
	sites = models.ManyToManyField(Site)

	class Meta:
		verbose_name_plural = 'topics'

	def __unicode__(self):
		return '%s' % self.title

	def get_absolute_url(self):
		return '/topics/%s/' % (self.slug)
		
	def live_story_set(self):
		""" Returns live stories for a topic """
		return self.stories.all().filter(status=1)

	def live_audio_set(self):
		""" Returns live audio for a topic """
		return self.audio.all().filter(status=1)

	def live_photo_set(self):
		""" Returns live photos for a topic """
		return self.photos.all().filter(status=1)

	def live_gallery_set(self):
		""" Returns live galleries for a topic """
		return self.galleries.all().filter(status=1)

	def live_video_set(self):
		""" Returns live videos for a topic """
		return self.videos.all().filter(status=1)
		
	def active_faculty_set(self):
		""" Returns active faculty for a topic """
		return self.faculty.filter(is_currently_employed=True)