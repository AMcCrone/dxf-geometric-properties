def format_properties_output(properties, ref_material_name, markdown=True):
    """
    Format section properties into a readable string
    
    Args:
        properties: Dictionary of section properties
        ref_material_name: Name of reference material
        markdown: Whether to format output as markdown (default True)
        
    Returns:
        String with formatted properties
    """
    # Extract properties
    area = properties['area']
    perimeter = properties['perimeter']
    cx, cy = properties['centroid']
    e_ixx = properties['e_ixx']
    e_iyy = properties['e_iyy']
    e_ixy = properties['e_ixy']
    ixx = properties['ixx']
    iyy = properties['iyy']
    ixy = properties['ixy']
    zxx_plus = properties['zxx_plus']
    zxx_minus = properties['zxx_minus']
    zyy_plus = properties['zyy_plus']
    zyy_minus = properties['zyy_minus']
    i1 = properties.get('i1', 0)
    i2 = properties.get('i2', 0)
    phi = properties.get('phi', 0)
    
    # Format output based on markdown parameter
    if markdown:
        bullet = "•"
        linebreak = "\n"
        bold_start = "**"
        bold_end = "**"
    else:
        bullet = "*"
        linebreak = "\n"
        bold_start = ""
        bold_end = ""
    
    # Build output string
    output = []
    
    # Basic properties
    output.append(f"{bold_start}Basic Properties:{bold_end}")
    output.append(f"{bullet} Area:                   {area:>12,.2f} mm²")
    output.append(f"{bullet} Perimeter:              {perimeter:>12,.2f} mm")
    output.append(f"{bullet} Centroid (X,Y):         ({cx:>6.2f}, {cy:>6.2f}) mm")
    output.append("")
    
    # Modulus-weighted properties
    output.append(f"{bold_start}Modulus-Weighted Properties:{bold_end}")
    output.append(f"{bullet} E·Ixx:                  {e_ixx:>12,.2f} N·mm²")
    output.append(f"{bullet} E·Iyy:                  {e_iyy:>12,.2f} N·mm²")
    output.append(f"{bullet} E·Ixy:                  {e_ixy:>12,.2f} N·mm²")
    output.append("")
    
    # Transformed properties
    output.append(f"{bold_start}Transformed Properties (Ref: {ref_material_name.capitalize()}):{bold_end}")
    output.append(f"{bullet} Transformed Ixx:        {ixx:>12,.2f} mm⁴")
    output.append(f"{bullet} Transformed Iyy:        {iyy:>12,.2f} mm⁴")
    output.append(f"{bullet} Transformed Ixy:        {ixy:>12,.2f} mm⁴")
    output.append("")
    
    # Section moduli
    output.append(f"{bold_start}Section Moduli:{bold_end}")
    output.append(f"{bullet} Transformed Zxx+ (T):   {zxx_plus:>12,.2f} mm³")
    output.append(f"{bullet} Transformed Zxx- (C):   {zxx_minus:>12,.2f} mm³")
    output.append(f"{bullet} Transformed Zyy+ (T):   {zyy_plus:>12,.2f} mm³")
    output.append(f"{bullet} Transformed Zyy- (C):   {zyy_minus:>12,.2f} mm³")
    output.append("")
    
    # Principal moments of inertia
    if i1 != 0 or i2 != 0:
        output.append(f"{bold_start}Principal Moments of Inertia:{bold_end}")
        output.append(f"{bullet} I1:                     {i1:>12,.2f} mm⁴")
        output.append(f"{bullet} I2:                     {i2:>12,.2f} mm⁴")
        output.append(f"{bullet} Principal Angle:        {phi:>12,.2f} degrees")
    
    return linebreak.join(output)
