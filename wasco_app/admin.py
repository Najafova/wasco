from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ['dev_id', 'battery', 'bin_state']
    search_fields = ['dev_id']
    list_filter = ['dev_id']

@admin.register(DeviceSettings)
class DeviceSettingsAdmin(admin.ModelAdmin):
    list_display = ['dev_id', 'latitude', 'longitude']
    search_fields = ['dev_id', 'latitude', 'longitude']
    list_filter = ['dev_id']


@admin.register(LogData)
class LogDataAdmin(admin.ModelAdmin):
    list_display = ['dev_id', 'battery', 'bin_state', 'request_time']
    search_fields = ['dev_id']
    list_filter = ['dev_id']