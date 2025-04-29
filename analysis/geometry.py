# analysis/geometry.py
from sectionproperties.pre import Material
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
import os

def create_geometry_from_dxf(dxf_filepath, material, spline_delta=0.01, degrees_per_segment=10.0):
    """
    Creates a geometry object from a DXF file with assigned material
    
    Args:
        dxf_filepath: Path to the DXF file
        material: Material object to assign to the geometry
        spline_delta: Spline sampling rate (smaller = more accurate)
        degrees_per_segment: Number of degrees discretized as a single line segment
        
    Returns:
        Geometry object with assigned material
    """
    if not os.path.exists(dxf_filepath):
        raise FileNotFoundError(f"DXF file not found: {dxf_filepath}")
    
    try:
        # Use the direct method from sectionproperties v3.9.0
        geometry = Geometry.from_dxf(
            dxf_filepath=dxf_filepath,
            spline_delta=spline_delta,
            degrees_per_segment=degrees_per_segment
        )
        
        # Assign material
        geometry.material = material
        
        return geometry
    except ImportError:
        raise ImportError(
            "Failed to load DXF file. Make sure you have installed the required dependencies:\n"
            "pip install cad_to_shapely==0.3.2 sectionproperties[dxf]==3.9.0"
        )
    except Exception as e:
        raise Exception(f"Error loading DXF file: {str(e)}")

def create_compound_geometry(components, mesh_size=20.0):
    """
    Creates a compound geometry from multiple DXF components
    
    Args:
        components: List of tuples (dxf_path, material) for all section components
        mesh_size: Mesh size for the geometry
        
    Returns:
        CompoundGeometry object with mesh created
    """
    if not components:
        raise ValueError("No components provided for compound geometry")
    
    # Get the first component
    first_path, first_material = components[0]
    
    try:
        # Create geometry with material for the first component
        first_geometry = create_geometry_from_dxf(first_path, first_material)
        
        if len(components) == 1:
            # If there's only one component, no need for CompoundGeometry
            geometry = first_geometry
        else:
            # Initialize list of geometries
            geometries = [first_geometry]
            
            # Add remaining components
            for dxf_path, material in components[1:]:
                # Create geometry with material
                geometry = create_geometry_from_dxf(dxf_path, material)
                geometries.append(geometry)
            
            # Create compound geometry using the constructor
            geometry = CompoundGeometry(geometries)
        
        # Create mesh - ensure mesh_size is a list
        if not isinstance(mesh_size, list):
            mesh_size = [mesh_size]
            
        geometry.create_mesh(mesh_sizes=mesh_size)
        
        return geometry
        
    except Exception as e:
        raise Exception(f"Error creating compound geometry: {str(e)}")
