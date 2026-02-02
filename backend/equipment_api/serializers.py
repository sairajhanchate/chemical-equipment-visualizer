"""
Serializers for Chemical Equipment Parameter Visualizer API
Handles conversion between Django models and JSON representations
"""

from rest_framework import serializers
from .models import EquipmentUpload, EquipmentData
import json


class EquipmentDataSerializer(serializers.ModelSerializer):
    """
    Serializer for individual equipment records.
    Used to represent equipment parameters in API responses.
    """
    
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class EquipmentUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for equipment upload metadata.
    Includes nested equipment records and computed statistics.
    """
    
    equipment_records = EquipmentDataSerializer(many=True, read_only=True)
    equipment_type_distribution_json = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentUpload
        fields = [
            'id',
            'csv_file',
            'uploaded_at',
            'total_equipment_count',
            'average_pressure',
            'average_temperature',
            'equipment_type_distribution',
            'equipment_type_distribution_json',
            'equipment_records'
        ]
        read_only_fields = [
            'uploaded_at',
            'total_equipment_count',
            'average_pressure',
            'average_temperature',
            'equipment_type_distribution'
        ]
    
    def get_equipment_type_distribution_json(self, obj):
        """
        Convert equipment type distribution from text to JSON object.
        Handles parsing errors gracefully.
        """
        try:
            if obj.equipment_type_distribution:
                return json.loads(obj.equipment_type_distribution)
            return {}
        except json.JSONDecodeError:
            return {}


class CSVUploadSerializer(serializers.Serializer):
    """
    Serializer for handling CSV file uploads.
    Validates file format and processes equipment data.
    """
    
    csv_file = serializers.FileField(help_text="CSV file containing equipment parameters")
    
    def validate_csv_file(self, value):
        """
        Validate that uploaded file is a CSV with proper extension.
        """
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are accepted. Please upload a .csv file.")
        
        # Additional validation: check file size (limit to 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("CSV file size must be less than 5MB.")
        
        return value
