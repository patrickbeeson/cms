from django.conf.urls.defaults import patterns, include, url
from cms.categories.models import Category
from django.views.generic import ListView, DetailView

urlpatterns = patterns('',
    (r'^(?P<slug>[-\w]+)/$', DetailView.as_view(
    	context_object_name = "category",
    	template_name_field = "template_name",
    	#template_name = "categories/category_detail.html",
    	model = Category,
    )),
	(r'^$', ListView.as_view(
		model = Category,
		context_object_name = "category_list",
		paginate_by = 15,
	)),
)