import datetime
import tagging

from django.db import models
from tagging.fields import TagField

from cms.categories.models import Category

class Document(models.Model):
	PDF = 1
	DOC = 2
	TXT = 3
	FILE_TYPES = (
		(PDF, 'PDF'),
		(DOC, 'DOC'),
		(TXT, 'TXT'),
	)
	updated_date = models.DateTimeField(auto_now=True)
	uploaded_date = models.DateTimeField(auto_now_add=True)
	file_type = models.IntegerField(choices=FILE_TYPES)
	title = models.CharField(max_length=250, help_text='Limited to 250 characters.')
	description = models.TextField(help_text='No HTML is allowed.', blank=True)
	document = models.FileField(upload_to='documents')
	tags = TagField(help_text="Separate tags with spaces.")
	categories = models.ManyToManyField(Category, limit_choices_to={'topic__category_ptr__isnull': True, 'eventtype__category_ptr__isnull': True}, blank=True)

	class Meta:
		ordering = ['-title']
		verbose_name_plural = 'documents'

	def __unicode__(self):
		return self.title