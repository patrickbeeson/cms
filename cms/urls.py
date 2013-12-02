from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap
from django.views.generic import RedirectView, TemplateView

from cms.press.models import Mention
from cms.news.models import Story
from cms.media.models import Audio, Gallery, Video, Photo
from cms.events.models import Event
from cms.views import HomePageView, RobotsView
from cms.news.feeds import LatestStories, LatestStoriesByCategory
from cms.events.feeds import UpcomingEvents, UpcomingEventsByEventType
from cms.jobs.feeds import LatestJobs
from cms.press.feeds import LatestMentions
from cms.sitemaps import NewsSitemap, EventsSitemap

from tagging.models import Tag

admin.autodiscover()

sitemaps = {
	'news': NewsSitemap,
	'events': EventsSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	
	(r'^$', HomePageView.as_view()),

	(r'^feeds/news/$', LatestStories()),
	(r'^feeds/categories/(?P<slug>[-\w]+)/$', LatestStoriesByCategory()),
	(r'^feeds/events/$', UpcomingEvents()),
	(r'^feeds/eventtypes/(?P<slug>[-\w]+)/$', UpcomingEventsByEventType()),
	(r'^feeds/jobs/$', LatestJobs()),
	(r'^feeds/press/$', LatestMentions()),

	(r'^contact/', include('contact_form.urls')),

	(r'^categories/', include('cms.categories.urls')),

	(r'^employees/', include('cms.employees.urls')),

	(r'^jobs/', include('cms.jobs.urls')),

	(r'^topics/', include('cms.topics.urls')),  

	(r'^news/', include('cms.news.urls')),

	(r'^events/', include('cms.events.urls')),

	(r'^audio/', include('cms.media.audio_urls')),

	(r'^photos/', include('cms.media.photo_urls')),

	(r'^galleries/', include('cms.media.gallery_urls')),

	(r'^videos/', include('cms.media.video_urls')),

	(r'^press/', include('cms.press.urls')),
    (r'^news/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Story.live.all().order_by('-pub_date'), 'template_name': 'news/stories_for_tag.html' }),
	(r'^audio/tags/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Audio, 'template_name': 'media/audio_for_tag.html' }),
	(r'^events/tags/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Event.current.all().order_by('event_date'), 'template_name': 'events/events_for_tag.html' }),
	(r'^photos/tags/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Photo, 'template_name': 'media/photos_for_tag.html' }),
	(r'^videos/tags/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Video, 'template_name': 'media/videos_for_tag.html' }),
	(r'^galleries/tags/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Gallery, 'template_name': 'media/galleries_for_tag.html' }),
                       
	(r'^search/$', TemplateView.as_view(
		template_name = "search/google_search_results.html"
	)),

	('^s/', include('shorturls.urls')),

	(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	(r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

	(r'^robots\.txt$', RobotsView.as_view()),

	(r'', include('django.contrib.flatpages.urls')),
)