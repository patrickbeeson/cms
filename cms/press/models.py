from django.db import models
from django.contrib.sites.models import Site

from cms.categories.models import Category
from cms.employees.models import Employee

import datetime

class Mention (models.Model):
	NEWSPAPER = 1
	TELEVISION = 2
	RADIO = 3
	MAGAZINE = 4
	WEBSITE = 5
	BLOG = 6
	TWITTER = 7
	FACEBOOK = 8
	TYPE_CHOICES = (
		(NEWSPAPER, 'Newspaper'),
		(TELEVISION, 'Television'),
		(RADIO, 'Radio'),
		(MAGAZINE, 'Magazine'),
		(WEBSITE, 'Website'),
		(BLOG, 'Blog'),
		(TWITTER, 'Twitter'),
		(FACEBOOK, 'Facebook'),
	)
	title = models.CharField(max_length="200", help_text="Limited to 200 characters.")
	pub_date = models.DateTimeField(help_text="The publication date of the mention.")
	source_name = models.CharField(max_length="200", help_text="Limited to 200 characters.", blank=True)
	source_type = models.IntegerField(choices=TYPE_CHOICES)
	mention = models.TextField(blank=True, help_text="A citation from the or description of the story or mention. No HTML is allowed.")
	URL = models.URLField(blank=True)
	categories = models.ManyToManyField(Category, limit_choices_to={'topic__category_ptr__isnull': True, 'eventtype__category_ptr__isnull': True}, blank=True)
	faculty_mentioned = models.ManyToManyField(Employee, limit_choices_to={'employee_type__in': [1, 4]}, blank=True)
	sites = models.ManyToManyField(Site)

	class Meta:
		ordering = ['-pub_date']
		verbose_name = "mention"
		verbose_name_plural = "mentions"

	def __unicode__(self):
		return self.title