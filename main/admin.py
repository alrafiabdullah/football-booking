from django.contrib import admin

from .models import Place

admin.sites.site.index_title = 'Football Admin'
admin.sites.site.site_header = 'Football Admin Panel'
admin.sites.site.site_title = 'Football Admin'


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'map_link')
    search_fields = ('name', 'address',)


admin.site.register(Place, PlaceAdmin)
