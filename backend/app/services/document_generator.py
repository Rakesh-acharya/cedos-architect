"""
Document Generation Service
"""

from typing import Dict, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

class DocumentGenerator:
    """Document Generation Service"""
    
    def generate_calculation_sheet(
        self,
        calculation_data: Dict,
        project_data: Dict
    ) -> bytes:
        """
        Generate structural calculation sheet PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph("STRUCTURAL CALCULATION SHEET", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Project Information
        story.append(Paragraph(f"<b>Project:</b> {project_data.get('project_name', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Project Code:</b> {project_data.get('project_code', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Calculation Code:</b> {calculation_data.get('calculation_code', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Input Parameters
        story.append(Paragraph("<b>INPUT PARAMETERS</b>", styles['Heading2']))
        input_params = calculation_data.get('input_parameters', {})
        for key, value in input_params.items():
            story.append(Paragraph(f"{key}: {value}", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Design Outputs
        story.append(Paragraph("<b>DESIGN OUTPUTS</b>", styles['Heading2']))
        design_outputs = calculation_data.get('design_outputs', {})
        for key, value in design_outputs.items():
            story.append(Paragraph(f"{key}: {value}", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Compliance Status
        compliance_status = calculation_data.get('compliance_status', 'N/A')
        status_color = colors.green if compliance_status == 'compliant' else colors.red
        story.append(Paragraph(
            f"<b>Compliance Status:</b> <font color='{status_color.hex}'> {compliance_status.upper()}</font>",
            styles['Normal']
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_boq_pdf(
        self,
        boq_data: Dict,
        project_data: Dict
    ) -> bytes:
        """
        Generate BOQ PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph("BILL OF QUANTITIES (BOQ)", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Project Information
        story.append(Paragraph(f"<b>Project:</b> {project_data.get('project_name', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>BOQ Code:</b> {boq_data.get('boq_code', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # BOQ Table
        items = boq_data.get('items', [])
        table_data = [['Item Code', 'Description', 'Quantity', 'Unit']]
        
        for item in items:
            table_data.append([
                item.get('item_code', ''),
                item.get('item_description', ''),
                str(item.get('quantity', 0)),
                item.get('unit', '')
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_cost_estimate_pdf(
        self,
        estimate_data: Dict,
        project_data: Dict
    ) -> bytes:
        """
        Generate cost estimate PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph("COST ESTIMATE", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Project Information
        story.append(Paragraph(f"<b>Project:</b> {project_data.get('project_name', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Estimate Code:</b> {estimate_data.get('estimate_code', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Cost Items Table
        items = estimate_data.get('items', [])
        table_data = [['Item Code', 'Description', 'Quantity', 'Unit', 'Rate', 'Amount']]
        
        for item in items:
            table_data.append([
                item.get('item_code', ''),
                item.get('item_description', ''),
                str(item.get('quantity', 0)),
                item.get('unit', ''),
                f"{item.get('unit_rate', 0):.2f}",
                f"{item.get('total_amount', 0):.2f}"
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Cost Summary
        story.append(Paragraph("<b>COST SUMMARY</b>", styles['Heading2']))
        story.append(Paragraph(f"Base Cost: ₹{estimate_data.get('base_cost', 0):,.2f}", styles['Normal']))
        story.append(Paragraph(f"Contingency: ₹{estimate_data.get('contingency_amount', 0):,.2f}", styles['Normal']))
        story.append(Paragraph(f"Escalation: ₹{estimate_data.get('escalation_amount', 0):,.2f}", styles['Normal']))
        story.append(Paragraph(f"GST: ₹{estimate_data.get('gst_amount', 0):,.2f}", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        total_cost = estimate_data.get('total_cost', 0)
        story.append(Paragraph(
            f"<b>TOTAL COST: ₹{total_cost:,.2f}</b>",
            ParagraphStyle(
                'TotalCost',
                parent=styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor('#1a237e'),
                fontName='Helvetica-Bold'
            )
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
