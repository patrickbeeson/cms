from django import template
from cms.news.models import Story
from cms.media.models import Photo, Video, Gallery

class VideoYearListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
		
	def render(self, context):
		context[self.varname] = Video.live.dates("created", "year").reverse()
		return ''

class GalleryYearListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Gallery.live.dates("created", "year").reverse()
		return ''

class PhotoYearListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Photo.live.dates("uploaded", "year").reverse()
		return ''

class StoryYearListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Story.live.dates("pub_date", "year").reverse()
		return ''

def do_get_video_year_list(parser, token):
	"""
	Gets a list of years in which videos are published.
	
	Syntax::
	
		{% get_video_year_list as [varname] %}
		
	Example::
	
		{% get_video_year_list as year_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return VideoYearListNode(bits[2])

def do_get_gallery_year_list(parser, token):
	"""
	Gets a list of years in which galleries are published.
	
	Syntax::
	
		{% get_gallery_year_list as [varname] %}
		
	Example::
	
		{% get_gallery_year_list as year_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return GalleryYearListNode(bits[2])

def do_get_photo_year_list(parser, token):
	"""
	Gets a list of years in which photos are published.
	
	Syntax::
	
		{% get_photo_year_list as [varname] %}
		
	Example::
	
		{% get_photo_year_list as year_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return PhotoYearListNode(bits[2])

def do_get_story_year_list(parser, token):
	"""
	Gets a list of years in which stories are published.
	
	Syntax::
	
		{% get_story_year_list as [varname] %}
		
	Example::
	
		{% get_story_year_list as year_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return StoryYearListNode(bits[2])

class VideoMonthListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Video.live.dates("created", "month").reverse()
		return ''

class GalleryMonthListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Gallery.live.dates("created", "month").reverse()
		return ''

class PhotoMonthListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Photo.live.dates("uploaded", "month").reverse()
		return ''

class StoryMonthListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Story.live.dates("pub_date", "month").reverse()
		return ''

def do_get_video_month_list(parser, token):
	"""
	Gets a list of months in which videos are published.
	
	Syntax::
	
		{% get_video_month_list as [varname] %}
		
	Example::
	
		{% get_video_month_list as month_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return VideoMonthListNode(bits[2])

def do_get_gallery_month_list(parser, token):
	"""
	Gets a list of months in which galleries are published.
	
	Syntax::
	
		{% get_gallery_month_list as [varname] %}
		
	Example::
	
		{% get_gallery_month_list as month_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return GalleryMonthListNode(bits[2])

def do_get_photo_month_list(parser, token):
	"""
	Gets a list of months in which photos are published.
	
	Syntax::
	
		{% get_photo_month_list as [varname] %}
		
	Example::
	
		{% get_photo_month_list as month_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return PhotoMonthListNode(bits[2])

def do_get_story_month_list(parser, token):
	"""
	Gets a list of months in which stories are published.
	
	Syntax::
	
		{% get_story_month_list as [varname] %}
		
	Example::
	
		{% get_story_month_list as month_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return StoryMonthListNode(bits[2])
	
register = template.Library()
register.tag('get_video_month_list', do_get_video_month_list)
register.tag('get_video_year_list', do_get_video_year_list)
register.tag('get_gallery_month_list', do_get_gallery_month_list)
register.tag('get_gallery_year_list', do_get_gallery_year_list)
register.tag('get_photo_month_list', do_get_photo_month_list)
register.tag('get_photo_year_list', do_get_photo_year_list)
register.tag('get_story_month_list', do_get_story_month_list)
register.tag('get_story_year_list', do_get_story_year_list)