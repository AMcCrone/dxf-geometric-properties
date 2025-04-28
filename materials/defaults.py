from sectionproperties.pre import Material

# Define default materials
DEFAULT_MATERIALS = {
    "aluminium": Material(
        name="Aluminium",
        elastic_modulus=70e3,
        poissons_ratio=0.33,
        density=2.7e-6,
        yield_strength=160,
        color="lightgrey",
    ),
    "steel": Material(
        name="Steel",
        elastic_modulus=210e3,
        poissons_ratio=0.3,
        density=7.85e-6,
        yield_strength=355,
        color="grey",
    ),
    "concrete": Material(
        name="Concrete",
        elastic_modulus=30e3,  # MPa (typical value)
        poissons_ratio=0.2,
        density=2.4e-6,  # kg/mm³
        yield_strength=25,  # MPa (compressive strength)
        color="lightblue",
    ),
    "timber": Material(
        name="Timber",
        elastic_modulus=11e3,  # MPa (typical value for structural timber)
        poissons_ratio=0.3,
        density=0.5e-6,  # kg/mm³
        yield_strength=20,  # MPa
        color="brown",
    ),
    "glass": Material(
        name="Glass",
        elastic_modulus=70e3,
        poissons_ratio=0.22,
        density=2.5e-6,
        yield_strength=50,
        color="lightcyan",
    )
}

def get_material_properties_text(material_name):
    """
    Returns a formatted string of material properties
    
    Args:
        material_name: Name of the material in DEFAULT_MATERIALS
        
    Returns:
        String with formatted material properties
    """
    if material_name.lower() not in DEFAULT_MATERIALS:
        return f"Material '{material_name}' not found in database"
        
    material = DEFAULT_MATERIALS[material_name.lower()]
    
    properties = [
        f"• Name: {material.name}",
        f"• Elastic Modulus: {material.elastic_modulus:,.2f} MPa",
        f"• Poisson's Ratio: {material.poissons_ratio:.3f}",
        f"• Density: {material.density * 1e6:,.3f} kg/m³",
        f"• Yield Strength: {material.yield_strength:,.2f} MPa"
    ]
    
    return "\n".join(properties)

def add_custom_material(name, elastic_modulus, poissons_ratio, density, yield_strength, color="lightgrey"):
    """
    Adds a custom material to DEFAULT_MATERIALS
    
    Args:
        name: Material name
        elastic_modulus: Elastic modulus in MPa
        poissons_ratio: Poisson's ratio
        density: Density in kg/mm³
        yield_strength: Yield strength in MPa
        color: Display color for the material
        
    Returns:
        None - updates DEFAULT_MATERIALS dictionary in place
    """
    safe_name = name.lower().replace(" ", "_")
    
    DEFAULT_MATERIALS[safe_name] = Material(
        name=name,
        elastic_modulus=float(elastic_modulus),
        poissons_ratio=float(poissons_ratio),
        density=float(density),
        yield_strength=float(yield_strength),
        color=color
    )
    
    return safe_name
