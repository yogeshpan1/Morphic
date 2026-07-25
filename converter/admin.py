from django.contrib import admin

from .models import ConversionJob


@admin.register(ConversionJob)
class ConversionJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_file_extension', 'target_format', 'status', 'created_at']
    list_filter = ['status', 'target_format']