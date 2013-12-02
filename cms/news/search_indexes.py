import datetime
from haystack.indexes import *
from haystack import site
from cms.news.models import Story


class StoryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    pub_date = DateTimeField(model_attr='pub_date')
    headline = CharField(model_attr='headline')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Story.live.filter(pub_date__lte=datetime.datetime.now())


site.register(Story, StoryIndex)