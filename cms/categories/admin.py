from django.contrib import admin
from cms.categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)