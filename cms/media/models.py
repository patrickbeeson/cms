from django.db import models
import datetime
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from markdown import markdown
from cms.categories.models import Category
from cms.employees.models import Employee
from tagging.fields import TagField

import tagging

class AudioFile(models.Model):
	MP3 = 1
	OGG = 2
	WAV = 3
	TYPE_CHOICES = (
		(MP3, 'mpeg'),
		(OGG, 'ogg'),
		(WAV, 'wav'),
	)
	encoding_type = models.IntegerField(choices=TYPE_CHOICES, default=MP3, help_text="Safari, Internet Explorer and Chrome use MP3, while FireFox and Opera use OGG and WAV. Note that mpeg is the same thing as mp3.")
	file = models.FileField(upload_to='audio')
	audio = models.ForeignKey('Audio')

class LiveAudioManager(models.Manager):
	def get_query_set(self):
		return super(LiveAudioManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Audio(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
	)
	title = models.CharField(max_length=250, help_text='Limited to 250 characters.')
	slug = models.SlugField(help_text='This field will automatically populate from the title.', unique_for_date='uploaded')
	thumbnail = models.ImageField(upload_to='images/audio_thumbs', blank=True, help_text='An image that will be used as a thumbnail. Minimum 150 pixels wide and tall.')
	thumbnail_alt_text = models.CharField(max_length=50, help_text='Limited to 50 characters.', blank=True)
	description = models.TextField(help_text='A brief description of the audio. No HTML is allowed.')
	tags = TagField(help_text="Separate tags with spaces.")
	producer = models.ForeignKey(User, limit_choices_to={'groups__name__exact': 'Producers'}, blank=True, null=True)
	one_off_producer = models.CharField(max_length=50, help_text='Limited to 50 characters.', blank=True)
	category = models.ManyToManyField(Category, limit_choices_to={'topic__category_ptr__isnull': True, 'eventtype__category_ptr__isnull': True})
	status = models.IntegerField(choices=STATUS_CHOICES, default=2, help_text="Only audio with a status of 'live' will be displayed publicly.")
	updated = models.DateTimeField(auto_now=True)
	uploaded = models.DateTimeField(default=datetime.datetime.now)
	faculty_profiled = models.ManyToManyField(Employee, limit_choices_to={'employee_type__lte': '1'}, blank=True)
	sites = models.ManyToManyField(Site)
	objects = models.Manager()
	live = LiveAudioManager()

	class Meta:
		db_table = 'media_audio'
		verbose_name_plural = 'audio'
		ordering = ['-uploaded']

	def __unicode__(self):
		return '%s' % self.title

	def get_absolute_url(self):
		return '/audio/%s/' % (self.slug)

	def live_story_set(self):
		""" Returns related live stories """
		from cms.news.models import Story
		return self.story_set.filter(status=Story.LIVE_STATUS)

	@property
	def related_audio_set(self):
		category_id_list = self.category.values_list("id", flat=True)
		return Audio.live.filter(category__id__in=category_id_list).exclude(id=self.id).distinct()[:5]

class LivePhotoManager(models.Manager):
	def get_query_set(self):
		return super(LivePhotoManager, self).get_query_set().filter(status=self.model.LIVE_STATUS).filter(is_aggregated=True)

class Photo(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
	)
	title = models.CharField(max_length=250, help_text='Limited to 250 characters. Will also be used for alt text.')
	slug = models.SlugField(help_text='This field will automatically populate from the title.', unique_for_date='uploaded')
	photo = models.ImageField(upload_to='images/photos', width_field='width', height_field='height', help_text="Please use JPG or PNG formats. Will populate the width and height fields on save.")
	uploaded = models.DateTimeField(default=datetime.datetime.now)
	updated = models.DateTimeField(auto_now=True)
	caption = models.TextField(help_text='A brief description of the photo. No HTML is allowed.')
	photographer = models.ForeignKey(User, limit_choices_to={'groups__name__exact': 'Photographers'}, blank=True, null=True)
	one_off_photographer = models.CharField(max_length=100, blank=True)
	width = models.PositiveIntegerField(blank=True, null=True)
	height = models.PositiveIntegerField(blank=True, null=True)
	alt_text = models.CharField(max_length=200, help_text="Limited to 100 characters. Used for displaying text in case image isn't viewable.")
	external_url = models.URLField(help_text="If the photo is located on an external Web site, please add the URL here.", blank=True)
	category = models.ManyToManyField(Category, limit_choices_to={'topic__category_ptr__isnull': True, 'eventtype__category_ptr__isnull': True})
	status = models.IntegerField(choices=STATUS_CHOICES, default=2, help_text="Only photos with a status of 'live' will be displayed publicly.")
	is_aggregated = models.BooleanField(default=True, help_text="Check this box to show photo in list-based views. Otherwise, it will only display on the object to which it's related.")
	tags = TagField(help_text="Separate tags with spaces.")
	sites = models.ManyToManyField(Site)
	objects = models.Manager()
	live = LivePhotoManager()

	class Meta:
		verbose_name = 'photo'
		verbose_name_plural = 'photos'
		ordering = ['-uploaded']

	def __unicode__(self):
		return '%s' % self.title

	def get_absolute_url(self):
		return '/photos/%s/%s/' % (self.uploaded.strftime('%Y/%b/%d').lower(), self.slug)

	def live_story_set(self):
		""" Returns related live stories """
		from cms.news.models import Story
		return self.related_photos.all().filter(status=Story.LIVE_STATUS)

	@property
	def related_photo_set(self):
		category_id_list = self.category.values_list("id", flat=True)
		return Photo.live.filter(category__id__in=category_id_list).exclude(id=self.id).distinct()[:5]

	@property
	def get_photo_orientation(self):
		if self.height > self.width:
			return "vertical"
		else:
			return "horizontal"

class LiveGalleryManager(models.Manager):
	def get_query_set(self):
		return super(LiveGalleryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Gallery(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
	)
	created = models.DateTimeField(default=datetime.datetime.now)
	slug = models.SlugField(help_text="This field will automatically populate from the title.", unique_for_date="created")
	title = models.CharField(max_length=250, help_text="Limited to 250 characters.")
	description = models.TextField(help_text='A brief description of the gallery. No HTML is allowed.')
	photos = models.ManyToManyField(Photo, through="GalleryPhoto", help_text='Note that the first photo selected will be used as the opening photo.')
	status = models.IntegerField(choices=STATUS_CHOICES, default=2, help_text="Only galleries with a status of 'live' will be displayed publicly.")
	category = models.ManyToManyField(Category, limit_choices_to={'topic__category_ptr__isnull': True, 'eventtype__category_ptr__isnull': True})
	objects = models.Manager()
	live = LiveGalleryManager()
	tags = TagField(help_text="Separate tags with spaces.")
	category = models.ManyToManyField(Category)
	sites = models.ManyToManyField(Site)

	class Meta:
		verbose_name_plural = 'galleries'
		ordering = ['-created']

	def __unicode__(self):
		return '%s' % self.title

	def get_absolute_url(self):
		return '/galleries/%s/%s/' % (self.created.strftime('%Y/%b/%d').lower(), self.slug)

	def live_story_set(self):
		""" Returns related live stories """
		from cms.news.models import Story
		return self.story_set.filter(status=Story.LIVE_STATUS)

	@property
	def related_gallery_set(self):
		category_id_list = self.category.values_list("id", flat=True)
		return Gallery.live.filter(category__id__in=category_id_list).exclude(id=self.id).distinct()[:5]

	@property
	def ordered_photos_for_gallery(self):
		""" Returns photos for a gallery with ordering applied. """
		return self.photos.order_by('galleryphoto__position')

	@property
	def get_thumbnail(self):
		""" Returns the first photo from the gallery to use as a thumbnail. """
		return self.photos.order_by('galleryphoto__position')[0]

class GalleryPhoto(models.Model):	
	gallery = models.ForeignKey(Gallery)
	photo = models.ForeignKey(Photo)
	position = models.IntegerField(help_text='A lower number denotes an earlier photo in the gallery. Positive integers only.')

	class Meta:
		ordering = ["position"]
		verbose_name_plural = 'gallery photos'
		verbose_name = 'gallery photo'

class LiveVideoManager(models.Manager):
	def get_query_set(self):
		return super(LiveVideoManager, self).get_query_set().filter(status=self.model.LIVE_STATUS).filter(is_aggregated=True).exclude(expires__lte=datetime.datetime.now())

class Video(models.Model):
	def expire_date():
		return datetime.datetime.now() + timedelta(days = 7)
		
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
	)
	YOUTUBE = 4
	VIMEO = 5
	EXTERNAL_CHOICES = (
		(YOUTUBE, 'YouTube'),
		(VIMEO, 'Vimeo'),
	)
	embed_code = models.TextField(help_text="Please paste the copied embed code into this field.")
	external_source = models.IntegerField(choices=EXTERNAL_CHOICES, default=YOUTUBE, help_text='Select the website where the video was published originally.')
	slug = models.SlugField(unique_for_date='created', help_text="This field will automatically populate from the title.")
	title = models.CharField(max_length=250, help_text="Limited to 250 characters.")
	created = models.DateTimeField(default=datetime.datetime.now)
	caption = models.TextField(help_text='A brief description of the video. No HTML is allowed.')
	videographer = models.ForeignKey(User, limit_choices_to={'groups__name__exact': 'Videographers'}, blank=True, null=True)
	one_off_videographer = models.CharField(max_length=100, blank=True)
	embed_width = models.PositiveIntegerField(help_text="The embed width in pixels. Default width is 630 pixels.", default=630)
	embed_height = models.PositiveIntegerField(help_text="The embed height in pixels. Default height is 315 pixels.", default=315)
	embed_url = models.URLField(help_text='The url of the video from the embed code. This is usually the iframe src attribute from the embed code.')
	thumbnail = models.ImageField(upload_to='images/video_thumbs', blank=True, null=True, help_text='An image that will be used as a thumbnail. Minimum 150 pixels wide and tall.')
	thumbnail_alt_text = models.CharField(max_length=50, help_text='Limited to 50 characters.', blank=True)
	external_url = models.URLField(help_text="The URL where the video was published originally.")
	status = models.IntegerField(choices=STATUS_CHOICES, default=2, help_text="Only videos with a status of 'live' will be displayed publicly.")
	category = models.ManyToManyField(Category, limit_choices_to={'topic__category_ptr__isnull': True, 'eventtype__category_ptr__isnull': True})
	tags = TagField(help_text="Separate tags with spaces.")
	category = models.ManyToManyField(Category)
	sites = models.ManyToManyField(Site)
	faculty_profiled = models.ManyToManyField(Employee, limit_choices_to={'employee_type__lte': '1'}, blank=True)
	is_aggregated = models.BooleanField(default=True, help_text="Check this box to show video in list-based views. Otherwise, it will only display on the object to which it's related.")
	expires = models.DateTimeField(blank=True, null=True, default=expire_date, help_text='This value is defaulted for seven days in the future. To leave this video up indefinitely, remove the default date and time.')
	objects = models.Manager()
	live = LiveVideoManager()

	class Meta:
		verbose_name_plural = 'videos'
		ordering = ['-created']
	
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '/videos/%s/%s/' % (self.created.strftime('%Y/%b/%d').lower(), self.slug)

	def live_story_set(self):
		""" Returns related live stories """
		from cms.news.models import Story
		return self.story_set.filter(status=Story.LIVE_STATUS)

	@property
	def is_expired(self):
		""" Returns true if the video has an expiration datetime less than or equal to the current datetime. Will return False if there is no expiration date. """
		if self.expires and self.expires <= datetime.datetime.now():
			return True
		else:
			return False

	@property
	def related_video_set(self):
		category_id_list = self.category.values_list("id", flat=True)
		return Video.live.filter(category__id__in=category_id_list).exclude(id=self.id).distinct()[:5]