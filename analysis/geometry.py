from sectionproperties.pre import Material
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
import os
from shapely.geometry import Polygon
from cad_to_shapely import DXFImporter

def create_geometry_from_dxf(dxf_filepath, material):
    """
    Creates a geometry object from a DXF file with assigned material using cad_to_shapely
    
    Args:
        dxf_filepath: Path to the DXF file
        material: Material object to assign to the geometry
        
    Returns:
        Geometry object with assigned material
    """
    if not os.path.exists(dxf_filepath):
        raise FileNotFoundError(f"DXF file not found: {dxf_filepath}")
    
    # Use cad_to_shapely to import DXF
    importer = DXFImporter(dxf_filepath)
    polygons = importer.process()
    
    # Convert each shapely polygon to a sectionproperties geometry
    geometries = []
    for poly in polygons:
        if isinstance(poly, Polygon) and poly.is_valid:
            # Extract coordinates from the Polygon
            exterior_coords = list(poly.exterior.coords)
            
            # Create a geometry from the polygon coordinates
            geom = Geometry(points=exterior_coords[:-1])  # Exclude last point (duplicate of first)
            geom.material = material
            geometries.append(geom)
    
    # If we have multiple polygons, create a compound geometry
    if len(geometries) > 1:
        compound_geom = CompoundGeometry(geometries)
        return compound_geom
    elif len(geometries) == 1:
        return geometries[0]
    else:
        raise ValueError(f"No valid polygons found in DXF file: {dxf_filepath}")

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
    
    # Initialize geometries list
    geometries = []
    
    # Process each component
    for dxf_path, material in components:
        # Create geometry with material
        geometry = create_geometry_from_dxf(dxf_path, material)
        
        # If the result is a compound geometry, extend our list with its components
        if isinstance(geometry, CompoundGeometry):
            geometries.extend(geometry.geometries)
        else:
            geometries.append(geometry)
    
    # Create compound geometry from all individual geometries
    compound_geom = CompoundGeometry(geometries)
    
    # Create mesh
    compound_geom.create_mesh(mesh_sizes=mesh_size)
    
    return compound_geom
