from django.db import models
from django.contrib.contenttypes.models import ContentType

class CategoryManager(models.Manager):
	def get_query_set(self):
		return super(CategoryManager, self).get_query_set().filter(topic__category_ptr__isnull = True, eventtype__category_ptr__isnull = True, placetype__category_ptr__isnull = True)

class Category(models.Model):
	title = models.CharField(max_length=50, help_text="Limited to 50 characters.")
	slug = models.SlugField(unique=True, help_text="Suggested value automatically generated from title. Must be unique.")
	description = models.TextField(help_text="A brief description of the content being categorized. No HTML is allowed.", blank=True)
	template_name = models.CharField(max_length=70, blank=True, help_text="Example: 'categories/grand_opening.html'. If this isn't provided, the system will use the default template specified for this object'.")
	categories = CategoryManager()
	objects = models.Manager()

	class Meta:
		ordering = ['title']
		verbose_name_plural = "categories"
		
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '/categories/%s/' % (self.slug)

	def live_story_set(self):
		""" Returns live stories for a category """
		from cms.news.models import Story
		return self.story_set.filter(status=Story.LIVE_STATUS)

	def live_audio_set(self):
		""" Returns live audio for a category """
		from cms.media.models import Audio
		return self.audio_set.filter(status=Audio.LIVE_STATUS)

	def live_photo_set(self):
		""" Returns live photos for a category """
		from cms.media.models import Photo
		return self.photo_set.filter(status=Photo.LIVE_STATUS).filter(is_aggregated=True)

	def live_gallery_set(self):
		""" Returns live galleries for a category """
		from cms.media.models import Gallery
		return self.gallery_set.filter(status=Gallery.LIVE_STATUS)

	def live_video_set(self):
		""" Returns live videos for a category """
		from cms.media.models import Video
		return self.video_set.filter(status=Video.LIVE_STATUS)