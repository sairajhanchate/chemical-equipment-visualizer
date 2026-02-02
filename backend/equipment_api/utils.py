"""
Utility functions for Chemical Equipment Parameter Visualizer
Includes PDF report generation using ReportLab
"""

import os
import json
from datetime import datetime
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_pdf_report(upload):
    """
    Generate a comprehensive PDF report for an equipment upload.
    Includes summary statistics, equipment type distribution, and detailed data table.
    
    Args:
        upload: EquipmentUpload model instance
        
    Returns:
        str: Path to generated PDF file
    """
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate unique filename
    pdf_filename = f'equipment_report_{upload.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    pdf_path = os.path.join(reports_dir, pdf_filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Chemical Equipment Parameter Report", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    metadata = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Upload ID:', str(upload.id)],
        ['Upload Date:', upload.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    metadata_table = Table(metadata, colWidths=[2.5*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics Section
    summary_heading = Paragraph("Summary Statistics", heading_style)
    story.append(summary_heading)
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(upload.total_equipment_count)],
        ['Average Pressure', f'{upload.average_pressure:.2f} bar'],
        ['Average Temperature', f'{upload.average_temperature:.2f} °C'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Equipment Type Distribution
    distribution_heading = Paragraph("Equipment Type Distribution", heading_style)
    story.append(distribution_heading)
    
    try:
        type_dist = json.loads(upload.equipment_type_distribution)
        dist_data = [['Equipment Type', 'Count']]
        for eq_type, count in type_dist.items():
            dist_data.append([str(eq_type), str(count)])
    except:
        dist_data = [['Equipment Type', 'Count'], ['No data available', '-']]
    
    dist_table = Table(dist_data, colWidths=[3*inch, 3.5*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f8f5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    story.append(dist_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Detailed Equipment Data
    detail_heading = Paragraph("Detailed Equipment Data", heading_style)
    story.append(detail_heading)
    
    # Get equipment records
    equipment_records = upload.equipment_records.all()
    
    equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
    
    for record in equipment_records[:20]:  # Limit to first 20 records to avoid overly long PDFs
        equipment_data.append([
            record.equipment_name[:20],  # Truncate long names
            record.equipment_type[:15],
            f'{record.flowrate:.1f}',
            f'{record.pressure:.1f}',
            f'{record.temperature:.1f}'
        ])
    
    if upload.total_equipment_count > 20:
        equipment_data.append(['...', '...', '...', '...', '...'])
        equipment_data.append([f'Showing 20 of {upload.total_equipment_count} records', '', '', '', ''])
    
    equipment_table = Table(equipment_data, colWidths=[1.5*inch, 1.3*inch, 1.1*inch, 1.1*inch, 1*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    story.append(equipment_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Footer note
    footer_text = Paragraph(
        "This report was generated by the Chemical Equipment Parameter Visualizer system. "
        "Data accuracy depends on the quality of the uploaded CSV file.",
        styles['Normal']
    )
    story.append(footer_text)
    
    # Build PDF
    doc.build(story)
    
    return pdf_path


def process_csv_file(csv_file):
    """
    Additional CSV processing utility if needed for complex operations.
    Currently, processing is handled directly in views.py using Pandas.
    """
    pass
