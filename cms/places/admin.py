from cms.places.models import PlaceType, City, Point, Place
from django.contrib import admin

class PlaceTypeAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug',)
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(PlaceType, PlaceTypeAdmin)

class CityAdmin(admin.ModelAdmin):
	list_display = ('city', 'state', 'country')
	prepopulated_fields = {'slug': ('city', 'state', 'country')}
	search_fields = ['city']
	fields = ('city', 'state', 'country', 'slug')

admin.site.register(City, CityAdmin)

class PointAdmin(admin.ModelAdmin):
	list_display = ('latitude', 'longitude', 'address', 'city', 'zip')

admin.site.register(Point, PointAdmin)

class PlaceAdmin(admin.ModelAdmin):
	list_display = ('name', 'prename',)
	list_filter = ('created',)
	search_fields = ('name', 'description')
	prepopulated_fields = {'slug': ('name',)}

	fieldsets = (
		(None, {
			'fields': ('name', 'slug', 'prename', 'point', 'nickname', 'description', 'created', 'place_types')
		}),
		('Attributes', {
			'fields': ('unit', 'parking', 'phone', 'external_URL', 'email')
		}),
		('Settings', {
			'fields': ('status',)
		}),
	)

admin.site.register(Place, PlaceAdmin)