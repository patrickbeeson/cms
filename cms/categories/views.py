from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.http import Http404

from cms.categories.models import Category
from cms.news.models import Story
from cms.media.models import Photo, Audio, Gallery, Video
from cms.topics.models import Topic
from cms.events.models import EventType, Event
from cms.places.models import PlaceType

# Functions for passing into extra context
def get_live_stories():
	return Story.live.all()

def get_current_events():
	return Event.current.all()

def get_live_audio():
	return Audio.live.all()

def get_live_photos():
	return Photo.live.all()

def get_live_galleries():
	return Gallery.live.all()

def get_live_videos():
	return Video.live.all()

def category_detail(request, slug):
	try:
		category = Category.objects.get(slug__iexact=slug)
	except Category.DoesNotExist:
		raise Http404()
	
	try:
		topic = category.topic
		raise Http404()
	except Topic.DoesNotExist:
		pass

	try:
		eventtype = category.eventtype
		raise Http404()
	except EventType.DoesNotExist:
		pass

	try:
		placetype = category.placetype
		raise Http404()
	except PlaceType.DoesNotExist:
		pass

	return object_list(
		request,
		queryset = Category.objects.all(),
		template_name = 'categories/category_detail.html',
		template_object_name = 'category',
		extra_context = {'category': category}
	)


def category_list(request):	
	return object_list(
		request,
		queryset = Category.categories.all(),
		template_name = 'categories/category_list.html',
		template_object_name = 'category',
		allow_empty = True,
	)