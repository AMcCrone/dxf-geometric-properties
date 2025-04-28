from sectionproperties.analysis import Section

def calculate_section_properties(compound_geom, ref_material=None):
    """
    Calculate section properties from a compound geometry
    
    Args:
        compound_geom: CompoundGeometry object with mesh created
        ref_material: Reference material for transformed properties
        
    Returns:
        tuple: (section, properties_dict)
            section: Section object
            properties_dict: Dictionary of calculated properties
    """
    # Create section and calculate properties
    section = Section(geometry=compound_geom)
    section.calculate_geometric_properties()
    section.calculate_plastic_properties()
    section.calculate_warping_properties()
    
    # Get basic properties
    perimeter = section.get_perimeter()
    area = section.get_area()
    
    # Get modulus-weighted properties
    e_ixx, e_iyy, e_ixy = section.get_eic()
    
    # Get transformed properties using reference elastic modulus
    ixx, iyy, ixy = section.get_eic(e_ref=ref_material) if ref_material else (e_ixx, e_iyy, e_ixy)
    
    # Get centroids
    cx, cy = section.get_c()
    
    # Get section moduli with reference material
    try:
        # Get elastic moduli with reference material
        zxx_plus, zxx_minus, zyy_plus, zyy_minus = section.get_ez(e_ref=ref_material) if ref_material else section.get_ez()
    except (ValueError, TypeError) as e:
        # Fallback method if needed
        zxx_plus = zxx_minus = zyy_plus = zyy_minus = 0
        print(f"Could not calculate section moduli: {str(e)}")
    
    # Calculate principal moments of inertia
    try:
        i1, i2, phi = section.get_principal_angles()
    except (ValueError, TypeError):
        i1 = i2 = phi = 0
    
    # Package results in a dictionary
    properties = {
        'area': area,
        'perimeter': perimeter,
        'centroid': (cx, cy),
        'e_ixx': e_ixx,
        'e_iyy': e_iyy,
        'e_ixy': e_ixy,
        'ixx': ixx,
        'iyy': iyy,
        'ixy': ixy,
        'zxx_plus': zxx_plus,
        'zxx_minus': zxx_minus,
        'zyy_plus': zyy_plus,
        'zyy_minus': zyy_minus,
        'i1': i1,
        'i2': i2,
        'phi': phi,
    }
    
    return section, properties
