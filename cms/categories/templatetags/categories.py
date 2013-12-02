from django import template
from cms.categories.models import Category

class CategoryListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Category.objects.all().filter(topic__category_ptr__isnull = True, eventtype__category_ptr__isnull = True, placetype__category_ptr__isnull = True)
		return ''

def do_get_category_list(parser, token):
	"""
	Gets a list of all event types, and passes it into a custom variable.
	
	Syntax::
	
		{% get_category_list as [varname] %}
	
	Example::
	
		{% get_category_list as eventtype_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return CategoryListNode(bits[2])

register = template.Library()
register.tag('get_category_list', do_get_category_list)