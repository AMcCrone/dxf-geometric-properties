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
    
    # Create geometry from DXF
    geometry = Geometry.from_dxf(dxf_filepath=dxf_filepath)
    
    # Assign material
    geometry.material = material
    
    return geometry

def create_compound_geometry(main_dxf_path, main_material, reinforcements=None, mesh_size=20):
    """
    Creates a compound geometry from a main DXF file and optional reinforcements
    
    Args:
        main_dxf_path: Path to the main DXF file
        main_material: Material object for the main section
        reinforcements: List of tuples (dxf_path, material) for reinforcements
        mesh_size: Mesh size for the geometry
        
    Returns:
        CompoundGeometry object with mesh created
    """
    # Create main geometry with material
    main_geom = create_geometry_from_dxf(main_dxf_path, main_material)
    
    # Initialize compound geometry with main section
    compound_geom = CompoundGeometry([main_geom])
    
    # Add reinforcements if provided
    if reinforcements:
        for reinf_path, reinf_material in reinforcements:
            # Create reinforcement geometry with material
            reinf_geom = create_geometry_from_dxf(reinf_path, reinf_material)
            # Add to compound geometry
            compound_geom += reinf_geom
    
    # Create mesh
    compound_geom.create_mesh(mesh_sizes=mesh_size)
    
    return compound_geom
