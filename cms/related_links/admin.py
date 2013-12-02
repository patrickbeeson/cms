from django.contrib.contenttypes import generic
from cms.related_links.models import RelatedLink
#from django.contrib import admin


class RelatedLinkInline(generic.GenericStackedInline):
    extra = 3
    model = RelatedLink

#class RelatedLinkAdmin(admin.ModelAdmin):
#	pass

#admin.site.register(RelatedLink, RelatedLinkAdmin)