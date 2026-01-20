"""
Blueprint Generator - Auto-generates CAD-like drawings from design data
"""

from typing import Dict, List, Optional
from reportlab.lib.pagesizes import A4, A3, A2
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing, Rect, Line, Circle, String
from reportlab.graphics import renderPDF
import io
import math

class BlueprintGenerator:
    """Blueprint Generator - Creates technical drawings from design calculations"""
    
    def __init__(self):
        self.scale_factor = 100  # 1 meter = 100 units in drawing
    
    def generate_structural_plan(
        self,
        project_data: Dict,
        calculations: List[Dict],
        page_size: str = "A2"
    ) -> bytes:
        """
        Generate structural plan view (top view)
        """
        if page_size == "A2":
            page_width, page_height = A2
        elif page_size == "A3":
            page_width, page_height = A3
        else:
            page_width, page_height = A4
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        
        # Title block
        self._draw_title_block(c, page_width, page_height, project_data)
        
        # Drawing area (leave margins)
        margin = 2 * cm
        drawing_width = page_width - 2 * margin
        drawing_height = page_height - 3 * cm - margin
        
        # Draw grid
        self._draw_grid(c, margin, margin, drawing_width, drawing_height)
        
        # Draw structural elements
        x_offset = margin
        y_offset = margin
        
        for calc in calculations:
            calc_type = calc.get("calculation_type", "")
            design_outputs = calc.get("design_outputs", {})
            
            if calc_type == "footing_design":
                self._draw_footing(c, x_offset, y_offset, design_outputs)
                x_offset += 5 * cm
            
            elif calc_type == "column_design":
                self._draw_column(c, x_offset, y_offset, design_outputs)
                x_offset += 3 * cm
            
            elif calc_type == "beam_design":
                self._draw_beam(c, x_offset, y_offset, design_outputs)
                x_offset += 4 * cm
        
        # Draw dimensions
        self._draw_dimensions(c, margin, margin, drawing_width, drawing_height)
        
        # Draw legend
        self._draw_legend(c, page_width - 4 * cm, margin + 1 * cm)
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_elevation_view(
        self,
        project_data: Dict,
        calculations: List[Dict],
        page_size: str = "A2"
    ) -> bytes:
        """
        Generate elevation view (side view)
        """
        if page_size == "A2":
            page_width, page_height = A2
        else:
            page_width, page_height = A3
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        
        # Title block
        self._draw_title_block(c, page_width, page_height, project_data, view_type="ELEVATION")
        
        margin = 2 * cm
        drawing_width = page_width - 2 * margin
        drawing_height = page_height - 3 * cm - margin
        
        # Draw elevation
        x_offset = margin
        y_offset = margin
        
        for calc in calculations:
            calc_type = calc.get("calculation_type", "")
            design_outputs = calc.get("design_outputs", {})
            
            if calc_type == "column_design":
                self._draw_column_elevation(c, x_offset, y_offset, design_outputs)
                x_offset += 3 * cm
            
            elif calc_type == "beam_design":
                self._draw_beam_elevation(c, x_offset, y_offset, design_outputs)
                x_offset += 4 * cm
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_section_view(
        self,
        project_data: Dict,
        calculation: Dict,
        page_size: str = "A3"
    ) -> bytes:
        """
        Generate section view
        """
        page_width, page_height = A3 if page_size == "A3" else A4
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        
        self._draw_title_block(c, page_width, page_height, project_data, view_type="SECTION")
        
        margin = 2 * cm
        calc_type = calculation.get("calculation_type", "")
        design_outputs = calculation.get("design_outputs", {})
        
        if calc_type == "footing_design":
            self._draw_footing_section(c, margin, margin, design_outputs)
        elif calc_type == "beam_design":
            self._draw_beam_section(c, margin, margin, design_outputs)
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_road_plan(
        self,
        project_data: Dict,
        road_design: Dict
    ) -> bytes:
        """
        Generate road plan view
        """
        page_width, page_height = A2
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        
        self._draw_title_block(c, page_width, page_height, project_data, view_type="ROAD PLAN")
        
        margin = 2 * cm
        drawing_width = page_width - 2 * margin
        drawing_height = page_height - 3 * cm - margin
        
        # Draw road centerline
        center_y = margin + drawing_height / 2
        c.setLineWidth(2)
        c.setStrokeColor(colors.black)
        c.line(margin, center_y, margin + drawing_width, center_y)
        
        # Draw lanes
        lane_width = road_design.get("lane_width", 3.75) * self.scale_factor / 10
        shoulder_width = road_design.get("shoulder_width", 2.0) * self.scale_factor / 10
        
        # Left lane
        c.setLineWidth(1)
        c.setDash([5, 5])
        c.line(margin, center_y - lane_width, margin + drawing_width, center_y - lane_width)
        c.line(margin, center_y + lane_width, margin + drawing_width, center_y + lane_width)
        
        # Shoulders
        c.setDash([2, 2])
        c.line(margin, center_y - lane_width - shoulder_width, 
               margin + drawing_width, center_y - lane_width - shoulder_width)
        c.line(margin, center_y + lane_width + shoulder_width, 
               margin + drawing_width, center_y + lane_width + shoulder_width)
        
        # Add dimensions
        self._draw_road_dimensions(c, margin, center_y, lane_width, shoulder_width)
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def _draw_title_block(self, c, page_width, page_height, project_data, view_type="PLAN"):
        """Draw title block"""
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, page_height - 1.5 * cm, 
                    f"{project_data.get('project_name', 'Project')} - {view_type}")
        
        c.setFont("Helvetica", 10)
        c.drawString(2 * cm, page_height - 2 * cm, 
                    f"Project Code: {project_data.get('project_code', 'N/A')}")
        c.drawString(2 * cm, page_height - 2.3 * cm, 
                    f"Scale: 1:100 | Date: {project_data.get('date', 'N/A')}")
    
    def _draw_grid(self, c, x, y, width, height, spacing=1*cm):
        """Draw grid lines"""
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.setDash([1, 4])
        
        # Vertical lines
        for i in range(int(width / spacing) + 1):
            c.line(x + i * spacing, y, x + i * spacing, y + height)
        
        # Horizontal lines
        for i in range(int(height / spacing) + 1):
            c.line(x, y + i * spacing, x + width, y + i * spacing)
    
    def _draw_footing(self, c, x, y, design_outputs):
        """Draw footing plan"""
        size = design_outputs.get("footing_size", 1.0) * self.scale_factor / 10
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(x, y, size, size, fill=0)
        
        # Column outline
        col_size = size * 0.2
        col_x = x + (size - col_size) / 2
        col_y = y + (size - col_size) / 2
        c.setFillColor(colors.darkgrey)
        c.rect(col_x, col_y, col_size, col_size, fill=1)
    
    def _draw_column(self, c, x, y, design_outputs):
        """Draw column plan"""
        size = design_outputs.get("column_size", 0.3) * self.scale_factor / 10
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.setFillColor(colors.darkgrey)
        c.rect(x, y, size, size, fill=1)
    
    def _draw_beam(self, c, x, y, design_outputs):
        """Draw beam plan"""
        width = design_outputs.get("beam_width", 0.23) * self.scale_factor / 10
        length = 3 * self.scale_factor / 10  # Assume 3m span
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(x, y, length, width, fill=0)
    
    def _draw_column_elevation(self, c, x, y, design_outputs):
        """Draw column elevation"""
        width = design_outputs.get("column_size", 0.3) * self.scale_factor / 10
        height = 3 * self.scale_factor / 10  # Assume 3m height
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(x, y, width, height, fill=0)
        
        # Reinforcement bars (simplified)
        c.setStrokeColor(colors.red)
        c.setLineWidth(1)
        bar_spacing = width / 4
        for i in range(1, 4):
            c.line(x + i * bar_spacing, y, x + i * bar_spacing, y + height)
    
    def _draw_beam_elevation(self, c, x, y, design_outputs):
        """Draw beam elevation"""
        width = design_outputs.get("beam_width", 0.23) * self.scale_factor / 10
        depth = design_outputs.get("overall_depth", 0.3) * self.scale_factor / 10
        length = 3 * self.scale_factor / 10
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(x, y, length, depth, fill=0)
    
    def _draw_footing_section(self, c, x, y, design_outputs):
        """Draw footing section"""
        size = design_outputs.get("footing_size", 1.0) * self.scale_factor / 10
        depth = design_outputs.get("effective_depth", 0.2) * self.scale_factor / 10
        
        # Footing
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(x, y, size, depth, fill=0)
        
        # Column
        col_size = size * 0.2
        col_x = x + (size - col_size) / 2
        c.rect(col_x, y + depth, col_size, depth * 0.5, fill=1)
    
    def _draw_beam_section(self, c, x, y, design_outputs):
        """Draw beam section"""
        width = design_outputs.get("beam_width", 0.23) * self.scale_factor / 10
        depth = design_outputs.get("overall_depth", 0.3) * self.scale_factor / 10
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(x, y, width, depth, fill=0)
    
    def _draw_dimensions(self, c, x, y, width, height):
        """Draw dimension lines"""
        c.setStrokeColor(colors.blue)
        c.setLineWidth(0.5)
        
        # Horizontal dimension
        dim_y = y - 0.5 * cm
        c.line(x, dim_y, x + width, dim_y)
        c.line(x, dim_y - 0.2 * cm, x, dim_y + 0.2 * cm)
        c.line(x + width, dim_y - 0.2 * cm, x + width, dim_y + 0.2 * cm)
        
        c.setFont("Helvetica", 8)
        c.drawString(x + width / 2 - 1 * cm, dim_y - 0.8 * cm, f"{width / cm:.1f} cm")
    
    def _draw_legend(self, c, x, y):
        """Draw legend"""
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, "LEGEND")
        
        y -= 0.5 * cm
        c.setFont("Helvetica", 8)
        items = [
            ("Concrete", colors.darkgrey),
            ("Steel", colors.red),
            ("Dimension", colors.blue)
        ]
        
        for item, color in items:
            c.setFillColor(color)
            c.rect(x, y - 0.2 * cm, 0.5 * cm, 0.3 * cm, fill=1)
            c.setFillColor(colors.black)
            c.drawString(x + 0.7 * cm, y, item)
            y -= 0.5 * cm
    
    def _draw_road_dimensions(self, c, x, center_y, lane_width, shoulder_width):
        """Draw road dimensions"""
        c.setStrokeColor(colors.blue)
        c.setLineWidth(0.5)
        
        # Lane width dimension
        dim_y = center_y - lane_width - shoulder_width - 1 * cm
        c.line(x, dim_y, x, center_y - lane_width - shoulder_width)
        c.line(x + 5 * cm, dim_y, x + 5 * cm, center_y - lane_width - shoulder_width)
        c.line(x, dim_y, x + 5 * cm, dim_y)
        
        c.setFont("Helvetica", 8)
        c.drawString(x + 2 * cm, dim_y - 0.3 * cm, f"Lane: {lane_width / (self.scale_factor/10):.2f}m")
