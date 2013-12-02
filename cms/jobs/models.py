from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sitemaps import ping_google

import datetime

import tagging
from tagging.fields import TagField

from markdown import markdown

class ActiveManager(models.Manager):
	def get_query_set(self):
		return super(ActiveManager, self).get_query_set().exclude(is_expired=True)

class Job(models.Model):
	title = models.CharField(max_length=100, help_text="Limited to 100 characters.")
	slug = models.SlugField(help_text='Will populate from the title')
	posting_number = models.IntegerField(blank=True, null=True, help_text='This should be the posting number from the listing.')
	created = models.DateField(help_text='Date for when this job post was created.', default=datetime.datetime.now)
	description = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a> for all text-formatting and links. No HTML is allowed')
	description_html = models.TextField(editable=False, blank=True)
	required_qualifications = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a> for all text-formatting and links. No HTML is allowed')
	required_qualifications_html = models.TextField(editable=False, blank=True)
	how_to_apply = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a> for all text-formatting and links. No HTML is allowed')
	how_to_apply_html = models.TextField(editable=False, blank=True)
	posting_end_date = models.DateField(help_text='Not displayed to the public.', blank=True, null=True)
	is_expired = models.BooleanField(blank=True, default=False)
	external_link = models.URLField(help_text="Link to job positing externally.", verify_exists=False)
	tags = TagField(help_text="Separate tags with spaces.")
	sites = models.ManyToManyField(Site)
	objects = models.Manager()
	active = ActiveManager()
	
	class Meta:
		ordering = ['title']
		verbose_name_plural = "jobs"
		
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '/jobs/%s/' % (self.id)

	def is_expired(self):
		"""Returns True if the job posting date is less than the current date."""
		return self.posting_end_date < datetime.date.today()

	def save(self, force_insert=False, force_update=False):
		self.description_html = markdown(self.description)
		self.required_qualifications_html = markdown(self.required_qualifications)
		self.how_to_apply_html = markdown(self.how_to_apply)
		super(Job, self).save(force_insert, force_update)
		try:
			ping_google()
		except Exception:
			pass