# analysis/geometry.py
from sectionproperties.pre import Material
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
import os

def create_geometry_from_dxf(dxf_filepath, material):
    """
    Creates a geometry object from a DXF file with assigned material
    
    Args:
        dxf_filepath: Path to the DXF file
        material: Material object to assign to the geometry
        
    Returns:
        Geometry object with assigned material
    """
    if not os.path.exists(dxf_filepath):
        raise FileNotFoundError(f"DXF file not found: {dxf_filepath}")
    
    # Use the direct method from sectionproperties v3.9.0
    geometry = Geometry.from_dxf(
        dxf_filepath=dxf_filepath,
        spline_delta=0.01,  # Default value, can be made configurable
        degrees_per_segment=10.0  # Default value, can be made configurable
    )
    
    # Assign material
    geometry.material = material
    
    return geometry

def create_compound_geometry(components, mesh_size=20):
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
    
    # Create geometry with material for the first component
    first_geometry = create_geometry_from_dxf(first_path, first_material)
    
    if len(components) == 1:
        # If there's only one component, no need for CompoundGeometry
        compound_geom = first_geometry
    else:
        # Initialize compound geometry with the first geometry
        geometries = [first_geometry]
        
        # Add remaining components
        for dxf_path, material in components[1:]:
            # Create geometry with material
            geometry = create_geometry_from_dxf(dxf_path, material)
            geometries.append(geometry)
        
        # Create compound geometry using the constructor
        compound_geom = CompoundGeometry(geometries)
    
    # Create mesh
    compound_geom.create_mesh(mesh_sizes=[mesh_size])
    
    return compound_geom
