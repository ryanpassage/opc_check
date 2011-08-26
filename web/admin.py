from web.models import Asset
from django.contrib import admin

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'collector', 'path', 'quality', 'bad_count', 'last_check', 'check_enabled')

admin.site.register(Asset, AssetAdmin)
