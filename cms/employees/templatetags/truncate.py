from django import template

register = template.Library()

#@register.filter("truncatecharacters")
def truncatecharacters(value, size):
	"""
	A filter to truncate a string by a given number of characters.
	
	Usage::
	
		{{ employee.first_name|truncatecharacters:1|escape }}
	"""
	return value[0:size]

register.filter(truncatecharacters)

#@register.filter("truncatecharacters_dot")
def truncatecharacters_dot(value, size):
	"""
	A filter to truncate a string by a given number of characters. Will display three periods after the truncation.
	
	Usage::
	
		{{ employee.first_name|truncatecharacters_dot:1|escape }}
	"""
	if len(value) > size and size > 3:
		return value[0:(size-3)] + '...'
	else:
		return value[0:size]
	
register.filter(truncatecharacters_dot)