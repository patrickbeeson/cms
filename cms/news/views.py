from django.views.generic import DateDetailView
from cms.news.models import Story
from django.contrib.auth.models import User

class StoryDetailView(DateDetailView):

	date_field = "pub_date"
	template_name = "news/story_detail.html"
	context_object_name = "story"
	slug_field = "slug"

	def get_queryset(self):
		stories = None
		if self.request.user.is_staff:
			stories = Story.objects.all()
		else:
			stories = Story.live.all()
		return stories