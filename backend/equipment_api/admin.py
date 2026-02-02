"""
Admin configuration for Chemical Equipment Parameter Visualizer
Registers models for Django admin interface with custom display options
"""

from django.contrib import admin
from .models import EquipmentUpload, EquipmentData


@admin.register(EquipmentUpload)
class EquipmentUploadAdmin(admin.ModelAdmin):
    """
    Admin interface for EquipmentUpload model.
    Displays key statistics and provides filtering options.
    """
    list_display = [
        'id',
        'uploaded_at',
        'total_equipment_count',
        'average_pressure',
        'average_temperature'
    ]
    list_filter = ['uploaded_at']
    search_fields = ['id']
    readonly_fields = [
        'uploaded_at',
        'total_equipment_count',
        'average_pressure',
        'average_temperature',
        'equipment_type_distribution'
    ]
    
    fieldsets = (
        ('File Information', {
            'fields': ('csv_file', 'uploaded_at')
        }),
        ('Statistics', {
            'fields': (
                'total_equipment_count',
                'average_pressure',
                'average_temperature',
                'equipment_type_distribution'
            )
        }),
    )


@admin.register(EquipmentData)
class EquipmentDataAdmin(admin.ModelAdmin):
    """
    Admin interface for EquipmentData model.
    Displays individual equipment records with filtering and search.
    """
    list_display = [
        'equipment_name',
        'equipment_type',
        'flowrate',
        'pressure',
        'temperature',
        'upload'
    ]
    list_filter = ['equipment_type', 'upload']
    search_fields = ['equipment_name', 'equipment_type']
    
    fieldsets = (
        ('Equipment Information', {
            'fields': ('upload', 'equipment_name', 'equipment_type')
        }),
        ('Parameters', {
            'fields': ('flowrate', 'pressure', 'temperature')
        }),
    )
