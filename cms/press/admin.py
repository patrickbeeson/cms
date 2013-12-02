from django.contrib import admin
from cms.press.models import Mention

class MentionAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date', 'source_type', 'source_name')
	list_filter = ('pub_date',)
	
admin.site.register(Mention, MentionAdmin)