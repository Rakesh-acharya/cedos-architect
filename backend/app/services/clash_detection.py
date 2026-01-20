"""
Clash Detection Service - Detect spatial conflicts between different systems
"""

from typing import Dict, List, Tuple
import math

class ClashDetectionService:
    """Clash Detection Service - Spatial conflict detection"""
    
    def detect_structural_clashes(
        self,
        structural_elements: List[Dict],
        mep_elements: List[Dict] = None,
        drainage_elements: List[Dict] = None
    ) -> Dict:
        """
        Detect clashes between structural and MEP/drainage elements
        """
        clashes = []
        
        # Check structural vs MEP
        if mep_elements:
            for struct in structural_elements:
                for mep in mep_elements:
                    clash = self._check_spatial_overlap(struct, mep)
                    if clash["is_clashing"]:
                        clashes.append({
                            "element_1": struct.get("name", "Unknown"),
                            "element_1_type": "structural",
                            "element_2": mep.get("name", "Unknown"),
                            "element_2_type": "mep",
                            "clash_type": clash["clash_type"],
                            "severity": "high",
                            "location": clash["location"]
                        })
        
        # Check structural vs drainage
        if drainage_elements:
            for struct in structural_elements:
                for drain in drainage_elements:
                    clash = self._check_spatial_overlap(struct, drain)
                    if clash["is_clashing"]:
                        clashes.append({
                            "element_1": struct.get("name", "Unknown"),
                            "element_1_type": "structural",
                            "element_2": drain.get("name", "Unknown"),
                            "element_2_type": "drainage",
                            "clash_type": clash["clash_type"],
                            "severity": "medium",
                            "location": clash["location"]
                        })
        
        return {
            "total_clashes": len(clashes),
            "high_severity": len([c for c in clashes if c["severity"] == "high"]),
            "medium_severity": len([c for c in clashes if c["severity"] == "medium"]),
            "low_severity": len([c for c in clashes if c["severity"] == "low"]),
            "clashes": clashes
        }
    
    def _check_spatial_overlap(self, element1: Dict, element2: Dict) -> Dict:
        """Check if two elements overlap spatially"""
        pos1 = element1.get("position", {})
        pos2 = element2.get("position", {})
        
        dim1 = element1.get("dimensions", {})
        dim2 = element2.get("dimensions", {})
        
        # Simplified 3D bounding box check
        x1_min = pos1.get("x", 0)
        x1_max = x1_min + dim1.get("length", 0)
        y1_min = pos1.get("y", 0)
        y1_max = y1_min + dim1.get("width", 0)
        z1_min = pos1.get("z", 0)
        z1_max = z1_min + dim1.get("height", 0)
        
        x2_min = pos2.get("x", 0)
        x2_max = x2_min + dim2.get("length", 0)
        y2_min = pos2.get("y", 0)
        y2_max = y2_min + dim2.get("width", 0)
        z2_min = pos2.get("z", 0)
        z2_max = z2_min + dim2.get("height", 0)
        
        # Check overlap
        x_overlap = not (x1_max < x2_min or x2_max < x1_min)
        y_overlap = not (y1_max < y2_min or y2_max < y1_min)
        z_overlap = not (z1_max < z2_min or z2_max < z1_min)
        
        is_clashing = x_overlap and y_overlap and z_overlap
        
        clash_type = "hard_clash" if is_clashing else "no_clash"
        
        if x_overlap and y_overlap and not z_overlap:
            clash_type = "clearance_clash"
        elif (x_overlap and y_overlap and z_overlap):
            # Calculate overlap volume
            overlap_volume = min(x1_max, x2_max) - max(x1_min, x2_min) * \
                           min(y1_max, y2_max) - max(y1_min, y2_min) * \
                           min(z1_max, z2_max) - max(z1_min, z2_min)
            if overlap_volume > 0.1:  # More than 0.1 m³
                clash_type = "hard_clash"
            else:
                clash_type = "soft_clash"
        
        return {
            "is_clashing": is_clashing,
            "clash_type": clash_type,
            "location": {
                "x": (max(x1_min, x2_min) + min(x1_max, x2_max)) / 2,
                "y": (max(y1_min, y2_min) + min(y1_max, y2_max)) / 2,
                "z": (max(z1_min, z2_min) + min(z1_max, z2_max)) / 2
            }
        }
    
    def suggest_clash_resolution(
        self,
        clash_data: Dict
    ) -> Dict:
        """Suggest resolution for detected clash"""
        element1_type = clash_data.get("element_1_type", "")
        element2_type = clash_data.get("element_2_type", "")
        clash_type = clash_data.get("clash_type", "")
        
        suggestions = []
        
        if clash_type == "hard_clash":
            if "structural" in element1_type and "mep" in element2_type:
                suggestions.append("Relocate MEP element to avoid structural member")
                suggestions.append("Penetrate structural member with proper reinforcement")
            elif "structural" in element1_type and "drainage" in element2_type:
                suggestions.append("Adjust drainage pipe alignment")
                suggestions.append("Install drainage before structural work")
        
        elif clash_type == "clearance_clash":
            suggestions.append("Increase clearance between elements")
            suggestions.append("Verify minimum clearance requirements per code")
        
        return {
            "clash_id": clash_data.get("element_1", ""),
            "suggested_resolutions": suggestions if suggestions else ["Review and resolve manually"],
            "priority": "high" if clash_type == "hard_clash" else "medium"
        }
