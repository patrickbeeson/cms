from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

from cms.jobs.models import Job

current_site = Site.objects.get_current()

class LatestJobs(Feed):
	description_template = 'feeds/jobs_description.html'
	title_template = 'feeds/jobs_title.html'
	title = "Latest jobs | %s" % current_site.name
	link = "http://somedomain.com/jobs/"
	description = "The latest job opportunities..."

	def items(self):
		return Job.active.all()[:10]
		
	def item_title(self, item):
		return item.title
		
	def item_description(self, item):
		return item.description