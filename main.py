# main.py
import streamlit as st
import os
import matplotlib.pyplot as plt
import tempfile
import uuid
import traceback

# Import from our project modules
from materials.defaults import DEFAULT_MATERIALS
from analysis.geometry import create_compound_geometry
from analysis.properties import calculate_section_properties
from utils.plotting import plot_mesh, plot_centroids_with_info
from utils.formatting import format_properties_output

def main():
    st.set_page_config(
        page_title="DXF Compound Section Analyzer",
        page_icon="📏",
        layout="wide"
    )
    
    st.title("DXF Compound Section Analyzer")
    st.markdown("Interactive tool for analyzing compound cross-sections with multiple materials")
    
    # Display version information
    st.sidebar.markdown("### Version Information")
    st.sidebar.info("Using sectionproperties v3.9.0 and cad_to_shapely v0.3.2")
    
    # Initialize session state for storing section components
    if 'section_components' not in st.session_state:
        st.session_state.section_components = []
    
    # Create temporary directory if it doesn't exist yet
    if 'temp_dir' not in st.session_state:
        st.session_state.temp_dir = tempfile.mkdtemp(prefix="dxf_analyzer_")
    
    # Sidebar for analysis settings
    with st.sidebar:
        st.header("Analysis Settings")
        
        # Mesh size
        mesh_size = st.slider(
            "Mesh size (smaller = finer mesh)",
            min_value=0.1,
            max_value=50.0,
            value=20.0,
            step=0.1,
            help="Smaller values create a finer mesh but increase computation time"
        )
        
        # Advanced DXF import settings
        with st.expander("Advanced DXF Import Settings"):
            spline_delta = st.slider(
                "Spline delta",
                min_value=0.001,
                max_value=0.1,
                value=0.01,
                step=0.001,
                format="%.3f",
                help="Affects spline sampling rate (smaller = more accurate but slower)"
            )
            
            degrees_per_segment = st.slider(
                "Degrees per segment",
                min_value=1.0,
                max_value=45.0,
                value=10.0,
                step=1.0,
                help="Number of degrees discretized as a single line segment"
            )
        
        # Reference material for transformed properties
        st.subheader("Reference Material")
        material_options = list(DEFAULT_MATERIALS.keys())
        ref_material = st.selectbox(
            "Select reference material for transformed properties",
            options=material_options,
            index=0  # Default to first material
        )
        
        # Analysis button
        analyze_button = st.button("Analyze Section", type="primary", use_container_width=True)
    
    # Main area - Component Management
    st.header("Section Components")
    
    # Form for adding a new component
    with st.form("add_component"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            dxf_file = st.file_uploader("Upload DXF file", type=["dxf"])
        
        with col2:
            material_options = list(DEFAULT_MATERIALS.keys())
            material = st.selectbox(
                "Select material",
                options=material_options
            )
        
        add_button = st.form_submit_button("Add Component")
        
        if add_button and dxf_file is not None:
            # Generate a unique filename
            unique_filename = f"{uuid.uuid4().hex}_{dxf_file.name}"
            file_path = os.path.join(st.session_state.temp_dir, unique_filename)
            
            # Write the file to disk
            with open(file_path, 'wb') as f:
                f.write(dxf_file.getvalue())
            
            # Add to the session state list
            st.session_state.section_components.append({
                "path": file_path,
                "material": material,
                "filename": dxf_file.name
            })
            
            st.success(f"Added component: {dxf_file.name} with {material} material")
            st.rerun()
    
    # Display current components
    if st.session_state.section_components:
        components_table = []
        for i, comp in enumerate(st.session_state.section_components):
            components_table.append({
                "Index": i + 1,
                "File": comp["filename"],
                "Material": comp["material"].capitalize()
            })
        
        st.table(components_table)
        
        # Option to remove components
        col1, col2 = st.columns([3, 1])
        with col1:
            component_to_remove = st.selectbox(
                "Select component to remove",
                options=range(1, len(st.session_state.section_components) + 1),
                format_func=lambda x: f"{x}. {st.session_state.section_components[x-1]['filename']}"
            )
        
        with col2:
            if st.button("Remove Selected Component"):
                # Get index (0-based)
                idx = component_to_remove - 1
                # Remove file
                if os.path.exists(st.session_state.section_components[idx]['path']):
                    os.unlink(st.session_state.section_components[idx]['path'])
                # Remove from list
                st.session_state.section_components.pop(idx)
                st.success(f"Component removed.")
                st.rerun()
    else:
        st.info("No components added yet. Add at least one DXF component to begin analysis.")
    
    # Create tabs for results and visualization
    tab1, tab2 = st.tabs(["Results", "Visualization"])
    
    # Perform analysis when button is clicked
    if analyze_button:
        if len(st.session_state.section_components) == 0:
            st.error("Please add at least one component before analyzing.")
        else:
            with st.spinner("Analyzing compound section..."):
                try:
                    # Create geometry from DXF files
                    components = [
                        (comp["path"], DEFAULT_MATERIALS[comp["material"]])
                        for comp in st.session_state.section_components
                    ]
                    
                    # Create compound geometry from all components
                    compound_geom = create_compound_geometry(
                        components, 
                        mesh_size=[mesh_size]  # Pass as list as required by API
                    )
                    
                    # Calculate section properties
                    section, properties = calculate_section_properties(
                        compound_geom, 
                        ref_material=DEFAULT_MATERIALS[ref_material]
                    )
                    
                    # Store results in session state
                    st.session_state.section = section
                    st.session_state.properties = properties
                    
                    # Show success message
                    st.success("Analysis completed successfully!")
                    
                except ImportError as e:
                    st.error(f"Import error: {str(e)}")
                    st.error("""
                    Please make sure you have the required packages installed:
                    ```
                    pip install sectionproperties[dxf]==3.9.0 cad_to_shapely==0.3.2
                    ```
                    """)
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    # Show more detailed error for debugging
                    with st.expander("Detailed Error Information"):
                        st.code(traceback.format_exc())
                    
                    st.error("""
                    Troubleshooting steps:
                    1. Verify closed, non-intersecting polylines in your DXF
                    2. Ensure Z=0 for all vertices (FLATTEN in CAD)
                    3. Try smaller mesh size
                    4. Check units are millimeters
                    5. Verify proper installation of dependencies
                    """)
    
    # Tab 1: Results
    with tab1:
        if 'properties' in st.session_state:
            properties = st.session_state.properties
            
            st.header("Section Properties")
            
            # Display formatted properties
            st.markdown(format_properties_output(properties, ref_material))
            
            # Download button for results
            result_text = format_properties_output(properties, ref_material, markdown=False)
            st.download_button(
                label="Download Results as TXT",
                data=result_text,
                file_name="section_properties.txt",
                mime="text/plain"
            )
            
        else:
            st.info("Click 'Analyze Section' to view results")
    
    # Tab 2: Visualization
    with tab2:
        if 'section' in st.session_state:
            section = st.session_state.section
            properties = st.session_state.properties
            
            st.header("Section Visualization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Section Mesh")
                fig1, ax1 = plt.subplots(figsize=(10, 6))
                plot_mesh(section, ax1)
                st.pyplot(fig1)
            
            with col2:
                st.subheader("Section Centroids")
                fig2, ax2 = plt.subplots(figsize=(10, 6))
                plot_centroids_with_info(section, properties, ax2)
                st.pyplot(fig2)
            
            # Option to display full results (advanced)
            with st.expander("Advanced Analysis Results"):
                st.text("This may take a moment to compute...")
                if st.button("Generate Full Results"):
                    try:
                        # Create matplotlib figure for results
                        fig, ax = plt.subplots(figsize=(12, 8))
                        section.plot_mesh(ax=ax, materials=True)
                        section.plot_centroids(ax=ax)
                        ax.set_title("Cross-Section Analysis")
                        ax.set_xlabel('x')
                        ax.set_ylabel('y')
                        ax.grid(True)
                        ax.set_aspect('equal')
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"Could not generate advanced visualization: {str(e)}")
                        with st.expander("Detailed Error Information"):
                            st.code(traceback.format_exc())
            
        else:
            st.info("Click 'Analyze Section' to view visualizations")
    
    # Cleanup temporary files when app shuts down
    def clean_temp_files():
        if 'section_components' in st.session_state:
            for comp in st.session_state.section_components:
                if os.path.exists(comp["path"]):
                    try:
                        os.unlink(comp["path"])
                    except Exception as e:
                        print(f"Failed to delete {comp['path']}: {e}")
    
    # Register cleanup function to run when session ends
    import atexit
    atexit.register(clean_temp_files)

if __name__ == "__main__":
    main()
