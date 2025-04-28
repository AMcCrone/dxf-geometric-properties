from sectionproperties.pre import Material
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
import os

def create_geometry_from_dxf(dxf_filepath, material):
    """
    Creates a geometry object from a DXF file with assigned material
    """
    if not os.path.exists(dxf_filepath):
        raise FileNotFoundError(f"DXF file not found: {dxf_filepath}")
    
    # Create geometry directly from DXF without intermediate steps
    geometry = Geometry.from_dxf(dxf_filepath=dxf_filepath)
    geometry.material = material
    
    return geometry

def create_compound_geometry(components, mesh_size=20):
    """
    Creates a compound geometry from multiple DXF components
    """
    if not components:
        raise ValueError("No components provided for compound geometry")
    
    # Initialize with an empty list
    geometries = []
    
    # Create geometry for each component
    for dxf_path, material in components:
        geometry = create_geometry_from_dxf(dxf_path, material)
        geometries.append(geometry)
    
    # Create compound geometry
    compound_geom = CompoundGeometry(geometries)
    compound_geom.create_mesh(mesh_sizes=mesh_size)
    
    return compound_geom
