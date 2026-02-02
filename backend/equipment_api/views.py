"""
API Views for Chemical Equipment Parameter Visualizer
Handles CSV uploads, data processing, statistics calculation, and PDF generation
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse, HttpResponse
from .models import EquipmentUpload, EquipmentData
from .serializers import CSVUploadSerializer, EquipmentUploadSerializer
from .utils import process_csv_file, generate_pdf_report
import pandas as pd
import json
import traceback


@api_view(['POST'])
def upload_csv(request):
    """
    Handle CSV file upload and process equipment data.
    Extracts parameters, calculates statistics, and stores in database.
    
    Expected CSV columns: Equipment Name, Type, Flowrate, Pressure, Temperature
    """
    serializer = CSVUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    csv_file = serializer.validated_data['csv_file']
    
    try:
        # Process CSV using Pandas
        df = pd.read_csv(csv_file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return Response(
                {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Clean data - remove rows with missing values
        df_clean = df.dropna(subset=required_columns)
        
        if len(df_clean) == 0:
            return Response(
                {'error': 'No valid data rows found in CSV after removing incomplete entries'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate statistics using Pandas
        total_count = len(df_clean)
        avg_pressure = float(df_clean['Pressure'].mean())
        avg_temperature = float(df_clean['Temperature'].mean())
        
        # Calculate equipment type distribution
        type_distribution = df_clean['Type'].value_counts().to_dict()
        type_distribution_json = json.dumps(type_distribution)
        
        # Create EquipmentUpload record
        upload = EquipmentUpload.objects.create(
            csv_file=csv_file,
            total_equipment_count=total_count,
            average_pressure=avg_pressure,
            average_temperature=avg_temperature,
            equipment_type_distribution=type_distribution_json
        )
        
        # Create individual EquipmentData records
        equipment_records = []
        for _, row in df_clean.iterrows():
            equipment_records.append(
                EquipmentData(
                    upload=upload,
                    equipment_name=str(row['Equipment Name']),
                    equipment_type=str(row['Type']),
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                )
            )
        
        # Bulk create for efficiency
        EquipmentData.objects.bulk_create(equipment_records)
        
        # Serialize and return response
        response_serializer = EquipmentUploadSerializer(upload)
        
        return Response({
            'message': 'CSV processed successfully',
            'data': response_serializer.data,
            'statistics': {
                'total_equipment': total_count,
                'average_pressure': round(avg_pressure, 2),
                'average_temperature': round(avg_temperature, 2),
                'equipment_types': type_distribution
            }
        }, status=status.HTTP_201_CREATED)
        
    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'The uploaded CSV file is empty'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except pd.errors.ParserError:
        return Response(
            {'error': 'Invalid CSV format. Please check the file structure'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except ValueError as e:
        return Response(
            {'error': f'Data validation error: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Log full traceback for debugging
        print(f"Error processing CSV: {traceback.format_exc()}")
        return Response(
            {'error': f'Server error while processing CSV: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_upload_history(request):
    """
    Retrieve the last 5 CSV uploads with their metadata and statistics.
    Returns upload history in reverse chronological order.
    """
    try:
        # Get last 5 uploads (already ordered by -uploaded_at in model Meta)
        recent_uploads = EquipmentUpload.objects.all()[:5]
        serializer = EquipmentUploadSerializer(recent_uploads, many=True)
        
        return Response({
            'count': len(serializer.data),
            'history': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error fetching upload history: {traceback.format_exc()}")
        return Response(
            {'error': f'Error retrieving upload history: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_upload_detail(request, upload_id):
    """
    Retrieve detailed information for a specific upload including all equipment records.
    """
    try:
        upload = EquipmentUpload.objects.get(id=upload_id)
        serializer = EquipmentUploadSerializer(upload)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except EquipmentUpload.DoesNotExist:
        return Response(
            {'error': f'Upload with ID {upload_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"Error fetching upload detail: {traceback.format_exc()}")
        return Response(
            {'error': f'Error retrieving upload details: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def generate_pdf(request, upload_id):
    """
    Generate and return a PDF report for a specific equipment upload.
    Report includes summary statistics and equipment data visualization.
    """
    try:
        upload = EquipmentUpload.objects.get(id=upload_id)
        
        # Generate PDF using utility function
        pdf_path = generate_pdf_report(upload)
        
        # Return PDF file as response
        return FileResponse(
            open(pdf_path, 'rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=f'equipment_report_{upload_id}.pdf'
        )
        
    except EquipmentUpload.DoesNotExist:
        return Response(
            {'error': f'Upload with ID {upload_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"Error generating PDF: {traceback.format_exc()}")
        return Response(
            {'error': f'Error generating PDF report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint to verify API is running.
    """
    return Response({
        'status': 'healthy',
        'message': 'Chemical Equipment API is operational'
    }, status=status.HTTP_200_OK)
