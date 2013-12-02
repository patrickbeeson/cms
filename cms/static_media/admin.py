from django.contrib import admin
from cms.static_media.models import Document

class DocumentAdmin(admin.ModelAdmin):
	date_hierarchy = 'uploaded_date'
	list_display = ('title', 'uploaded_date', 'file_type', 'document',)
	search_fields = ['title', 'description']
	list_filter = ('uploaded_date', 'file_type')

admin.site.register(Document, DocumentAdmin)