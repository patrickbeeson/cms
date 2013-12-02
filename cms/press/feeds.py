import datetime

from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site

from cms.press.models import Mention

current_site = Site.objects.get_current()

class LatestMentions(Feed):
	description_template = 'feeds/press_description.html'
	title_template = 'feeds/press_title.html'
	title = "Latest press mentions | %s" % current_site.name
	link = "http://somedomain.com/press/"
	description = "The latest press mentions..."

	def items(self):
		return Mention.objects.order_by('-pub_date')[:15]
		
	def item_title(self, item):
		return item.title

	def item_link(self, item):
		return item.URL

	def item_pubdate(self, item):
		return item.pub_date