from django.conf.urls.defaults import patterns, include, url
from cms.topics.models import Topic
from django.views.generic import ListView, DetailView

urlpatterns = patterns('',
	(r'^$', ListView.as_view(
		queryset = Topic.objects.all().order_by('-title'),
		context_object_name = "topic_list",
		template_name = "topics/topic_list.html",
	)),
	(r'^(?P<slug>[-\w]+)/$', DetailView.as_view(
		model = Topic,
		context_object_name = "topic",
		template_name = "topics/topic_detail.html",
	)),
)