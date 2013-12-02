import datetime

from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

from cms.news.models import Story
from cms.categories.models import Category

current_site = Site.objects.get_current()

class LatestStories(Feed):
	description_template = 'feeds/news_description.html'
	title_template = 'feeds/news_title.html'
	title = "Latest news | %s" % current_site.name
	link = "http://somedomain.com/news/"
	description = "Latest news and information..."

	def items(self):
		return Story.live.filter(pub_date__lte=datetime.datetime.now())[:10]
		
	def item_title(self, item):
		return item.title
		
	def item_description(self, item):
		return item.description

	def item_pubdate(self, item):
		return item.pub_date
        
class LatestStoriesByCategory(Feed):
	description_template = 'feeds/categories_description.html'
	title_template = 'feeds/categories_title.html'
	
	def get_object(self, request, slug):
		return get_object_or_404(Category, slug=slug)
		
	def title(self, obj):
		return "Stories for %s category | %s" % (obj.title, current_site.name)
	
	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return obj.get_absolute_url()
	
	def description(self, obj):
		return "%s" % obj.description

	def items(self, obj):
		return Story.live.filter(categories__slug__exact=obj.slug).order_by('-pub_date')[:10]