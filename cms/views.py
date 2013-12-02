from django.views.generic import TemplateView

from cms.news.models import Story
from cms.events.models import Event
from cms.featured.models import StoryList, FeaturedStory, Poster, PosterItem
from cms.press.models import Mention

class HomePageView(TemplateView):
	
	template_name = "home.html"

	def get_context_data(self, **kwargs):
		context = super(HomePageView, self).get_context_data(**kwargs)
		context['event_list'] = Event.current.all().order_by('event_date')
		context['story_list'] = Story.live.all().order_by('-pub_date')[:5]
		context['press_list'] = Mention.objects.all().order_by('-pub_date')[:5]
		context['poster_list'] = PosterItem.objects.filter(poster__name__iexact='homepage')
		context['topstories_list'] = FeaturedStory.objects.filter(story_list__name__iexact='top_stories')
		return context

class RobotsView(TemplateView):
	
	template_name = "robots.txt"
	
	def render_to_response(self, context, **kwargs):
		return super(RobotsView, self).render_to_response(context, content_type='text/plain', **kwargs)