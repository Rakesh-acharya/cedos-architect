"""
Hydrology & Hydraulic Analysis Service - Advanced water flow and drainage calculations
"""

from typing import Dict, List
import math

class HydrologyService:
    """Hydrology & Hydraulic Analysis Service"""
    
    def calculate_runoff_using_rational_method(
        self,
        catchment_area: float,  # hectares
        rainfall_intensity: float,  # mm/hr
        runoff_coefficient: float,
        time_of_concentration: float = 15.0  # minutes
    ) -> Dict:
        """
        Calculate runoff using Rational Method (IS 1742)
        Q = C * I * A / 360
        """
        # Convert area to m²
        area_m2 = catchment_area * 10000
        
        # Calculate peak discharge (m³/s)
        discharge = (runoff_coefficient * rainfall_intensity * area_m2) / 360
        
        return {
            "catchment_area_hectares": catchment_area,
            "catchment_area_m2": area_m2,
            "rainfall_intensity_mm_hr": rainfall_intensity,
            "runoff_coefficient": runoff_coefficient,
            "peak_discharge_m3_s": round(discharge, 3),
            "time_of_concentration_min": time_of_concentration,
            "method": "Rational Method",
            "code_standard": "IS 1742:1983"
        }
    
    def design_open_channel(
        self,
        discharge: float,  # m³/s
        channel_slope: float,  # m/m
        manning_roughness: float = 0.013,  # For concrete
        channel_type: str = "rectangular"
    ) -> Dict:
        """
        Design open channel using Manning's equation
        Q = (1/n) * A * R^(2/3) * S^(1/2)
        """
        # For rectangular channel: Q = (1/n) * b * d * (b*d/(b+2d))^(2/3) * S^(1/2)
        
        # Iterative solution (simplified - using approximation)
        # Assume aspect ratio b/d = 2
        # d = (Q * n / (b * S^0.5))^(3/5) * ((b+2d)/b)^(2/5)
        
        # Simplified approach: assume depth
        depth = 1.0  # Start with 1m
        
        for _ in range(10):  # Iterate to find solution
            if channel_type == "rectangular":
                # Assume width = 2 * depth
                width = 2 * depth
                area = width * depth
                wetted_perimeter = width + 2 * depth
                hydraulic_radius = area / wetted_perimeter
                
                # Calculate discharge
                calculated_q = (1 / manning_roughness) * area * (hydraulic_radius ** (2/3)) * (channel_slope ** 0.5)
                
                # Adjust depth
                if calculated_q < discharge:
                    depth *= 1.1
                elif calculated_q > discharge * 1.01:
                    depth *= 0.9
                else:
                    break
        
        # Calculate velocity
        velocity = discharge / area
        
        # Check for erosion (max velocity)
        max_velocity = {
            "concrete": 6.0,  # m/s
            "earth": 2.0,
            "rock": 10.0
        }
        
        channel_material = "concrete"  # Default
        max_allowed_velocity = max_velocity.get(channel_material, 5.0)
        is_erosion_safe = velocity <= max_allowed_velocity
        
        return {
            "channel_type": channel_type,
            "design_discharge": discharge,
            "channel_slope": channel_slope,
            "channel_width": round(width, 2),
            "channel_depth": round(depth, 2),
            "flow_velocity": round(velocity, 2),
            "hydraulic_radius": round(hydraulic_radius, 3),
            "wetted_perimeter": round(wetted_perimeter, 2),
            "is_erosion_safe": is_erosion_safe,
            "manning_roughness": manning_roughness,
            "code_standard": "IS 10430:2000"
        }
    
    def calculate_flood_routing(
        self,
        inflow_hydrograph: List[float],
        storage_capacity: float,  # m³
        outlet_capacity: float,  # m³/s
        time_interval: float = 1.0  # hours
    ) -> Dict:
        """
        Calculate flood routing through reservoir/storage
        Simplified storage routing method
        """
        outflow_hydrograph = []
        storage_levels = []
        current_storage = 0.0
        
        for inflow in inflow_hydrograph:
            # Storage change
            net_inflow = inflow - outlet_capacity
            storage_change = net_inflow * time_interval * 3600  # Convert to m³
            
            current_storage = max(0, min(storage_capacity, current_storage + storage_change))
            
            # Outflow (limited by outlet capacity and storage)
            if current_storage > 0:
                outflow = min(outlet_capacity, current_storage / (time_interval * 3600))
            else:
                outflow = 0
            
            outflow_hydrograph.append(round(outflow, 3))
            storage_levels.append(round(current_storage, 2))
        
        peak_outflow = max(outflow_hydrograph) if outflow_hydrograph else 0
        peak_inflow = max(inflow_hydrograph) if inflow_hydrograph else 0
        attenuation = peak_inflow - peak_outflow
        
        return {
            "inflow_peak": peak_inflow,
            "outflow_peak": peak_outflow,
            "attenuation": round(attenuation, 3),
            "attenuation_percentage": round((attenuation / peak_inflow * 100), 2) if peak_inflow > 0 else 0,
            "outflow_hydrograph": outflow_hydrograph,
            "storage_levels": storage_levels,
            "max_storage_used": max(storage_levels) if storage_levels else 0,
            "storage_utilization_percentage": round((max(storage_levels) / storage_capacity * 100), 2) if storage_levels and storage_capacity > 0 else 0
        }
    
    def design_stormwater_detention_pond(
        self,
        catchment_area: float,  # hectares
        design_rainfall: float,  # mm
        required_detention_time: float = 24.0,  # hours
        infiltration_rate: float = 0.0  # mm/hr
    ) -> Dict:
        """
        Design stormwater detention pond
        """
        # Calculate runoff volume
        runoff_coefficient = 0.7  # Urban area
        area_m2 = catchment_area * 10000
        runoff_volume = (runoff_coefficient * design_rainfall * area_m2) / 1000  # m³
        
        # Detention storage required
        detention_volume = runoff_volume * 0.8  # 80% detention (simplified)
        
        # Pond dimensions (assuming rectangular)
        pond_depth = 2.0  # meters
        pond_area_required = detention_volume / pond_depth
        
        # Calculate side dimensions (assuming square)
        pond_side = math.sqrt(pond_area_required)
        
        # Outlet design (simplified)
        outlet_discharge = detention_volume / (required_detention_time * 3600)  # m³/s
        
        return {
            "catchment_area_hectares": catchment_area,
            "design_rainfall_mm": design_rainfall,
            "runoff_volume_m3": round(runoff_volume, 2),
            "detention_volume_m3": round(detention_volume, 2),
            "pond_depth_m": pond_depth,
            "pond_area_m2": round(pond_area_required, 2),
            "pond_side_length_m": round(pond_side, 2),
            "required_outlet_capacity_m3_s": round(outlet_discharge, 3),
            "detention_time_hours": required_detention_time,
            "code_standard": "IS 1742:1983"
        }
