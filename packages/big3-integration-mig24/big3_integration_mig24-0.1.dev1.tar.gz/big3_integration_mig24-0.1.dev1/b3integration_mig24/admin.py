from django.contrib import admin

from .models import Settings
from big3_data_main_app.custom_admin import custom_admin_site


@admin.register(Settings, site=custom_admin_site)
class SettingsAdmin(admin.ModelAdmin):
    pass
