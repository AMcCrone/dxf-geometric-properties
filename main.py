import streamlit as st
import os
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile

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
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Section Configuration")
        
        # Main DXF file upload
        st.subheader("Main Section")
        main_dxf_file = st.file_uploader("Upload main DXF file", type=["dxf"])
        
        # Material selection for main section
        material_options = list(DEFAULT_MATERIALS.keys())
        main_material = st.selectbox(
            "Select material for main section",
            options=material_options,
            index=0
        )
        
        # Mesh size
        mesh_size = st.slider(
            "Mesh size (smaller = finer mesh)",
            min_value=0.1,
            max_value=50.0,
            value=20.0,
            step=0.1,
            help="Smaller values create a finer mesh but increase computation time"
        )
        
        # Reference material for transformed properties
        st.subheader("Reference Material")
        ref_material = st.selectbox(
            "Select reference material for transformed properties",
            options=material_options,
            index=material_options.index(main_material)
        )
    
    # Main area
    if main_dxf_file is None:
        st.info("Please upload a main DXF file to begin analysis")
        return
    
    # Create tabs for adding reinforcements and viewing results
    tab1, tab2, tab3 = st.tabs(["Add Reinforcements", "Results", "Visualization"])
    
    # Save uploaded file to a temporary file
    with NamedTemporaryFile(suffix=".dxf", delete=False) as tmp_main:
        tmp_main.write(main_dxf_file.getvalue())
        main_dxf_path = tmp_main.name
    
    # Initialize reinforcements list to store configuration
    if 'reinforcements' not in st.session_state:
        st.session_state.reinforcements = []

    # Tab 1: Add Reinforcements
    with tab1:
        st.header("Add Reinforcement Sections")
        
        # Form for adding a new reinforcement
        with st.form("add_reinforcement"):
            reinf_dxf_file = st.file_uploader("Upload reinforcement DXF file", type=["dxf"])
            reinf_material = st.selectbox(
                "Select material for reinforcement",
                options=material_options
            )
            
            add_button = st.form_submit_button("Add Reinforcement")
            
            if add_button and reinf_dxf_file is not None:
                # Save reinforcement file to temporary file
                with NamedTemporaryFile(suffix=".dxf", delete=False) as tmp_reinf:
                    tmp_reinf.write(reinf_dxf_file.getvalue())
                    reinf_dxf_path = tmp_reinf.name
                
                # Add to the session state list
                st.session_state.reinforcements.append({
                    "path": reinf_dxf_path,
                    "material": reinf_material,
                    "filename": reinf_dxf_file.name
                })
                
                st.success(f"Added reinforcement: {reinf_dxf_file.name} with {reinf_material} material")
        
        # Display current reinforcements
        if st.session_state.reinforcements:
            st.subheader("Current Reinforcements")
            for i, reinf in enumerate(st.session_state.reinforcements):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.text(f"{i+1}. {reinf['filename']}")
                with col2:
                    st.text(reinf['material'].capitalize())
                with col3:
                    if st.button("Remove", key=f"remove_{i}"):
                        # Remove file
                        if os.path.exists(reinf['path']):
                            os.unlink(reinf['path'])
                        # Remove from list
                        st.session_state.reinforcements.pop(i)
                        st.rerun()
        else:
            st.info("No reinforcements added yet")
    
    # Create compound geometry and calculate properties when user clicks "Analyze"
    analyze_button = st.sidebar.button("Analyze Section", type="primary", use_container_width=True)
    
    if analyze_button:
        with st.spinner("Analyzing section..."):
            try:
                # Create geometry from DXF files
                compound_geom = create_compound_geometry(
                    main_dxf_path=main_dxf_path,
                    main_material=DEFAULT_MATERIALS[main_material],
                    reinforcements=[
                        (r["path"], DEFAULT_MATERIALS[r["material"]])
                        for r in st.session_state.reinforcements
                    ],
                    mesh_size=mesh_size
                )
                
                # Calculate section properties
                section, properties = calculate_section_properties(
                    compound_geom, 
                    ref_material=DEFAULT_MATERIALS[ref_material]
                )
                
                # Store results in session state
                st.session_state.section = section
                st.session_state.properties = properties
                
                # Switch to Results tab
                st.experimental_rerun()
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.error("""
                Troubleshooting steps:
                1. Verify closed, non-intersecting polylines
                2. Ensure Z=0 for all vertices (FLATTEN in CAD)
                3. Try smaller mesh size
                4. Check units are millimeters
                """)
    
    # Tab 2: Results
    with tab2:
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
    
    # Tab 3: Visualization
    with tab3:
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
                    # Create display and convert to an image
                    section.display_results()
                    # Note: Streamlit doesn't support the interactive display
                    # that sectionproperties uses, so we might need to modify this
                    st.warning("This functionality needs to be modified for Streamlit")
            
        else:
            st.info("Click 'Analyze Section' to view visualizations")
    
    # Cleanup temporary files when app shuts down
    if main_dxf_file is not None:
        if os.path.exists(main_dxf_path):
            try:
                os.unlink(main_dxf_path)
            except:
                pass

if __name__ == "__main__":
    main()
