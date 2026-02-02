"""
Models for Chemical Equipment Parameter Visualizer
Stores metadata and statistics for uploaded equipment CSV files
"""

from django.db import models
from django.utils import timezone


class EquipmentUpload(models.Model):
    """
    Model to store metadata for each uploaded CSV file containing equipment parameters.
    Tracks equipment specifications and calculated statistics.
    """
    
    # File metadata
    csv_file = models.FileField(upload_to='csvs/', help_text="Uploaded CSV file")
    uploaded_at = models.DateTimeField(default=timezone.now, help_text="Timestamp of upload")
    
    # Statistical data computed from CSV
    total_equipment_count = models.IntegerField(default=0, help_text="Total number of equipment entries")
    average_pressure = models.FloatField(default=0.0, help_text="Average pressure across all equipment (bar)")
    average_temperature = models.FloatField(default=0.0, help_text="Average temperature across all equipment (°C)")
    
    # Equipment type distribution stored as JSON-like text
    equipment_type_distribution = models.TextField(
        blank=True, 
        help_text="Distribution of equipment types in JSON format"
    )
    
    class Meta:
        ordering = ['-uploaded_at']  # Most recent uploads first
        verbose_name = "Equipment Upload"
        verbose_name_plural = "Equipment Uploads"
    
    def __str__(self):
        return f"Upload {self.id} - {self.total_equipment_count} equipment - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class EquipmentData(models.Model):
    """
    Model to store individual equipment records parsed from CSV.
    Each row represents one piece of equipment with its parameters.
    """
    
    upload = models.ForeignKey(
        EquipmentUpload, 
        on_delete=models.CASCADE, 
        related_name='equipment_records',
        help_text="Reference to the parent upload batch"
    )
    
    # Equipment parameters from CSV
    equipment_name = models.CharField(max_length=200, help_text="Name/ID of the equipment")
    equipment_type = models.CharField(max_length=100, help_text="Type/category of equipment")
    flowrate = models.FloatField(help_text="Flowrate in L/min or specified units")
    pressure = models.FloatField(help_text="Operating pressure in bar")
    temperature = models.FloatField(help_text="Operating temperature in °C")
    
    class Meta:
        ordering = ['equipment_name']
        verbose_name = "Equipment Data"
        verbose_name_plural = "Equipment Data"
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
