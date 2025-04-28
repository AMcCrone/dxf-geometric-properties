import matplotlib.pyplot as plt

def plot_mesh(section, ax=None):
    """
    Plot the mesh of a section
    
    Args:
        section: Section object
        ax: Matplotlib axis to plot on (optional)
        
    Returns:
        ax: Matplotlib axis with the plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    section.plot_mesh(ax=ax)
    ax.set_title("Section Mesh")
    ax.set_aspect('equal')
    
    return ax

def plot_centroids_with_info(section, properties, ax=None):
    """
    Plot centroids with inertia information
    
    Args:
        section: Section object
        properties: Dictionary of section properties
        ax: Matplotlib axis to plot on (optional)
        
    Returns:
        ax: Matplotlib axis with the plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    section.plot_centroids(ax=ax)
    ax.set_title("Section Centroids")
    ax.set_aspect('equal')
    
    # Compute section modulus as the minimum of zxx_plus and zxx_minus
    section_modulus = min(properties['zxx_plus'], properties['zxx_minus'])
    
    # Add inertia information
    info_text = (
        f"Area = {properties['area']:,.2f} mm²\n"
        f"Ixx = {properties['ixx']:,.2f} mm⁴\n"
        f"Iyy = {properties['iyy']:,.2f} mm⁴\n"
        f"Section Modulus = {section_modulus:,.2f} mm³"
    )
    
    # Overlay text information in the top left of the plot
    ax.text(0.05, 0.95, info_text,
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.7))
    
    return ax

def plot_stress_contour(section, moment_x=0, moment_y=0, ax=None):
    """
    Plot stress contour for given moments
    
    Args:
        section: Section object
        moment_x: Applied moment about x-axis (optional)
        moment_y: Applied moment about y-axis (optional)
        ax: Matplotlib axis to plot on (optional)
        
    Returns:
        ax: Matplotlib axis with the plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    if moment_x != 0 or moment_y != 0:
        # Calculate stresses for given moments
        section.calculate_stress(mx=moment_x, my=moment_y)
        # Plot stress contours
        section.plot_stress_mz(ax=ax)
    else:
        ax.text(0.5, 0.5, "Set non-zero moments to see stress contours",
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
    
    ax.set_title("Stress Contour")
    ax.set_aspect('equal')
    
    return ax
