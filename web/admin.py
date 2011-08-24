from web.models import Asset
from django.contrib import admin

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'collector', 'path', 'quality', 'last_check')

admin.site.register(Asset, AssetAdmin)
