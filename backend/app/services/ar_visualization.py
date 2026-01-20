"""
AR Visualization Service - Generates AR-ready data for camera-based blueprint overlay
"""

from typing import Dict, List, Optional, Tuple
import json
import math

class ARVisualizationService:
    """
    AR Visualization Service
    Generates data for Augmented Reality blueprint overlay using device camera
    """
    
    def __init__(self):
        self.marker_size = 0.2  # 20cm marker size
        self.scale_factor = 1.0
    
    def generate_ar_data(
        self,
        project_data: Dict,
        calculations: List[Dict],
        site_dimensions: Dict,
        marker_positions: List[Tuple[float, float, float]] = None
    ) -> Dict:
        """
        Generate AR visualization data
        
        Args:
            project_data: Project information
            calculations: List of design calculations
            site_dimensions: Site dimensions (length, width, height)
            marker_positions: Optional marker positions for AR tracking
        
        Returns:
            AR data structure for frontend
        """
        ar_data = {
            "project_id": project_data.get("id"),
            "project_name": project_data.get("project_name"),
            "site_dimensions": site_dimensions,
            "elements": [],
            "markers": [],
            "scale": self.scale_factor,
            "coordinate_system": "local",  # Local site coordinate system
            "ar_mode": "marker_based" if marker_positions else "markerless"
        }
        
        # Generate structural elements for AR
        x_offset = 0
        y_offset = 0
        
        for calc in calculations:
            calc_type = calc.get("calculation_type", "")
            design_outputs = calc.get("design_outputs", {})
            
            element = self._create_ar_element(calc_type, design_outputs, x_offset, y_offset)
            if element:
                ar_data["elements"].append(element)
                x_offset += element.get("width", 0) + 1.0  # 1m spacing
        
        # Generate AR markers if provided
        if marker_positions:
            for i, (x, y, z) in enumerate(marker_positions):
                ar_data["markers"].append({
                    "id": f"marker_{i}",
                    "position": {"x": x, "y": y, "z": z},
                    "size": self.marker_size,
                    "type": "corner" if i < 4 else "reference"
                })
        
        return ar_data
    
    def _create_ar_element(
        self,
        calc_type: str,
        design_outputs: Dict,
        x_offset: float,
        y_offset: float
    ) -> Optional[Dict]:
        """Create AR element from calculation"""
        
        if calc_type == "footing_design":
            size = design_outputs.get("footing_size", 1.0)
            depth = design_outputs.get("effective_depth", 0.2)
            
            return {
                "type": "footing",
                "position": {"x": x_offset, "y": y_offset, "z": 0},
                "dimensions": {"width": size, "length": size, "height": depth},
                "material": "concrete",
                "color": [0.5, 0.5, 0.5, 0.8],  # RGBA
                "wireframe": True,
                "show_dimensions": True
            }
        
        elif calc_type == "column_design":
            size = design_outputs.get("column_size", 0.3)
            height = 3.0  # Default height
            
            return {
                "type": "column",
                "position": {"x": x_offset, "y": y_offset, "z": 0},
                "dimensions": {"width": size, "length": size, "height": height},
                "material": "concrete",
                "color": [0.6, 0.6, 0.6, 0.7],
                "wireframe": True,
                "show_reinforcement": True
            }
        
        elif calc_type == "beam_design":
            width = design_outputs.get("beam_width", 0.23)
            depth = design_outputs.get("overall_depth", 0.3)
            length = 3.0  # Default span
            
            return {
                "type": "beam",
                "position": {"x": x_offset, "y": y_offset, "z": height},
                "dimensions": {"width": width, "length": length, "height": depth},
                "material": "concrete",
                "color": [0.7, 0.7, 0.7, 0.6],
                "wireframe": True,
                "orientation": "horizontal"
            }
        
        elif calc_type == "slab_design":
            thickness = design_outputs.get("slab_thickness", 0.1)
            area = 10.0  # Default area
            
            return {
                "type": "slab",
                "position": {"x": x_offset, "y": y_offset, "z": 0},
                "dimensions": {"width": math.sqrt(area), "length": math.sqrt(area), "height": thickness},
                "material": "concrete",
                "color": [0.8, 0.8, 0.8, 0.5],
                "wireframe": False,
                "show_reinforcement": True
            }
        
        return None
    
    def generate_ar_markers_config(
        self,
        site_corners: List[Tuple[float, float, float]]
    ) -> Dict:
        """
        Generate AR marker configuration for site corners
        """
        if len(site_corners) < 4:
            # Generate default corners if not provided
            site_corners = [
                (0, 0, 0),
                (10, 0, 0),
                (10, 10, 0),
                (0, 10, 0)
            ]
        
        markers = []
        for i, (x, y, z) in enumerate(site_corners):
            markers.append({
                "id": f"corner_{i}",
                "position": {"x": x, "y": y, "z": z},
                "type": "corner",
                "size": self.marker_size,
                "pattern": f"pattern_{i}",  # AR marker pattern ID
                "description": f"Site corner {i+1}"
            })
        
        return {
            "markers": markers,
            "coordinate_system": {
                "origin": {"x": 0, "y": 0, "z": 0},
                "axes": {"x": "east", "y": "north", "z": "up"}
            }
        }
    
    def calculate_ar_scale(
        self,
        camera_fov: float,
        marker_distance: float,
        marker_size: float
    ) -> float:
        """
        Calculate scale factor for AR overlay based on camera parameters
        """
        # Simplified scale calculation
        # In real implementation, this would use computer vision
        scale = (marker_distance * math.tan(math.radians(camera_fov / 2))) / marker_size
        return scale
    
    def generate_ar_instructions(
        self,
        project_data: Dict
    ) -> Dict:
        """
        Generate AR setup instructions
        """
        return {
            "setup_steps": [
                "1. Place AR markers at site corners (provided in markers config)",
                "2. Open AR view in mobile browser",
                "3. Allow camera access",
                "4. Point camera at markers to initialize AR",
                "5. Blueprint will overlay on real-world view",
                "6. Walk around to view from different angles"
            ],
            "requirements": {
                "device": "Mobile phone with camera",
                "browser": "Chrome/Safari with WebXR support",
                "markers": "Print AR markers from markers config",
                "lighting": "Good lighting conditions"
            },
            "features": [
                "Real-time blueprint overlay",
                "Scale-accurate visualization",
                "3D element rendering",
                "Dimension display",
                "Material visualization"
            ]
        }
