from django.conf.urls.defaults import patterns, include, url
from cms.press.models import Mention
from django.views.generic import ListView

urlpatterns = patterns('',
	(r'^$', ListView.as_view(
		queryset = Mention.objects.all().order_by('-pub_date'),
		context_object_name = "mention_list",
		template_name = "press/mention_list.html",
		paginate_by = 15,
	)),
)