import os
import streamlit as st
import pandas as pd
from PIL import Image

# Import custom scripts with exact file names
from scripts.parse_pdf import parse_drawing_pdf
from scripts.run_audit import run_compliance_audit
from scripts.generator_3d import generate_3d_building_model
from scripts.generator_3d import generate_3d_building_model, load_rooms_and_openings
# Page Configuration
st.set_page_config(
    page_title="AI Architectural Drawing Audit Agent",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ AI Architectural Drawing & Code Audit Agent")
st.caption("Automated Plan Review & Code Compliance Engine for PA UCC (2021 IBC/PA Statutory Amendments)")

# Sidebar Setup
st.sidebar.header("Configuration")
jurisdiction = st.sidebar.selectbox(
    "Select Governing Building Code Jurisdiction:",
    ["2021 PA UCC (Pennsylvania Uniform Construction Code)", "2021 International Building Code (IBC)"]
)

# File Upload or Default Sample PDF
uploaded_file = st.sidebar.file_uploader("Upload Architectural Drawing (PDF)", type=["pdf"])

output_dir = "output_data"
os.makedirs(output_dir, exist_ok=True)

if uploaded_file is not None:
    target_pdf = os.path.join(output_dir, uploaded_file.name)
    with open(target_pdf, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")
else:
    target_pdf = "sample_plan_A101.pdf"
    st.sidebar.info("No file uploaded. Using default sample drawing: sample_plan_A101.pdf")

# Rules path matching run_audit configuration
rules_path = "config/pennsylvania_ucc_2021.json"
if not os.path.exists(rules_path) and os.path.exists("rules/pa_ucc_2021_rules.json"):
    rules_path = "rules/pa_ucc_2021_rules.json"

json_output_path = os.path.join(output_dir, "plan_text.json")

# Parse Drawing PDF
try:
    parse_drawing_pdf(target_pdf, json_output_path, output_dir)
except Exception as e:
    st.error(f"Error parsing PDF drawing: {e}")

# Layout with Tabs: 2D Audit vs 3D Model View
tab1, tab2 = st.tabs(["📋 Compliance Audit Report", "🧊 Interactive 3D Model"])

with tab1:
    st.header("Architectural Building Code Compliance Audit Report")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📐 Blueprint Preview")
        show_flags = st.checkbox("Show Visual Compliance Flags", value=True)
        
        # Matches exact sheet image output name from parse_pdf.py
        preview_img_path = os.path.join(output_dir, "sheet_page_1.png")
        if os.path.exists(preview_img_path):
            img = Image.open(preview_img_path)
            st.image(img, caption="TEST DRAWING SHEET A-101: Floor Plan & Egress Layout")
        else:
            st.warning("Blueprint preview image not generated yet.")

    with col2:
        run_audit = st.button("🚀 Run Full Compliance Audit")
        if run_audit:
            audit_report_path = os.path.join(output_dir, "audit_report.md")
            try:
                # Execute compliance audit
                run_compliance_audit(json_output_path, rules_path, audit_report_path)
                
                # Read generated markdown report file
                if os.path.exists(audit_report_path):
                    with open(audit_report_path, "r") as f:
                        report_markdown = f.read()
                    st.success("Audit Complete!")
                    st.markdown(report_markdown)
                else:
                    st.error("Audit completed, but audit_report.md was not found.")
            except Exception as audit_err:
                st.error(f"Error running compliance audit: {audit_err}")
        else:
            st.info("Click **'🚀 Run Full Compliance Audit'** above to generate the full PA UCC report.")

with tab2:
    st.subheader("🧊 Interactive 3D Architectural Extrusion Viewer")
    st.info("💡 Tip: Click and drag with your mouse to rotate, zoom, and pan around the 3D model.")
    
    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    
    with col_ctrl1:
        wall_height = st.slider("Adjust Story Height (Z-Axis Extrusion in feet)", min_value=2.0, max_value=8.0, value=3.2, step=0.2)
    
    with col_ctrl2:
        render_mode = st.selectbox("Render View Mode:", ["Textured Solid", "Wireframe / Transparent", "Compliance Heatmap"])

    # Dynamically load rooms and openings from parsed JSON
    dynamic_rooms, dynamic_openings = load_rooms_and_openings(json_output_path, default_height=wall_height)
    
    # Generate 3D model with cutouts
    fig_3d = generate_3d_building_model(rooms_data=dynamic_rooms, openings_data=dynamic_openings, wall_height=wall_height)
    st.plotly_chart(fig_3d)