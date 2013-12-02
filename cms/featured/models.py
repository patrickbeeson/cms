from django.db import models
from django.contrib.sites.models import Site

from cms.news.models import Story
from cms.media.models import Photo

import datetime

class StoryList(models.Model):
	name = models.CharField(max_length=200, help_text="Limited to 200 characters.")
	live_date = models.DateTimeField(default=datetime.datetime.now)
	site = models.ForeignKey(Site)

	class Meta:
		verbose_name = 'Story list'
		verbose_name_plural = 'Story lists'
		
	def __unicode__(self):
		return self.name

class FeaturedStory(models.Model):
	story = models.ForeignKey(Story, limit_choices_to={'status__lte': 1})
	story_list = models.ForeignKey(StoryList)
	
	class Meta:
		verbose_name = 'Featured story'
		verbose_name_plural = 'Featured stories'
		ordering = ['id']
		
	def __unicode__(self):
		return self.story.headline

class Poster(models.Model):
	name = models.CharField(max_length=200)
	live_date = models.DateTimeField(default=datetime.datetime.now)
	site = models.ForeignKey(Site)

	class Meta:
		verbose_name = 'Poster'
		verbose_name_plural = 'Posters'
	
	def __unicode__(self):
		return self.name

class PosterItem(models.Model):
	LEFT = 1
	RIGHT = 2
	BOTTOM = 3
	ORIENTATION_CHOICES = (
		(LEFT, 'Left'),
		(RIGHT, 'Right'),
		(BOTTOM, 'Bottom'),
	)
	title = models.CharField(max_length=250, help_text="Limited to 250 characters.")
	tease = models.CharField(max_length=250, help_text="Limited to 250 characters.")
	link = models.URLField()
	image = models.ForeignKey(Photo, limit_choices_to={'status__lte': 1})
	poster = models.ForeignKey(Poster)
	orientation = models.IntegerField(choices=ORIENTATION_CHOICES, default=BOTTOM, help_text="This option determines where the title and subhead will be displayed on the poster image.")
	
	class Meta:
		verbose_name = 'Poster item'
		verbose_name_plural = 'Poster items'
		ordering = ['id']
	
	def __unicode__(self):
		return self.title