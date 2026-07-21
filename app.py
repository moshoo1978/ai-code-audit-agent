import os
import streamlit as st
import pandas as pd
from PIL import Image

from scripts.parse_pdf import parse_drawing_pdf
from scripts.run_audit import run_compliance_audit
from scripts.generator_3d import generate_3d_building_model, load_rooms_and_openings, export_to_obj
from scripts.export_pdf import generate_pdf_report
from scripts.diff_engine import generate_plan_diff

st.set_page_config(
    page_title="AI Architectural Drawing Audit Agent",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ AI Architectural Drawing & Code Audit Agent")
st.caption("Automated Plan Review & Code Compliance Engine for PA UCC (2021 IBC/PA Statutory Amendments)")

output_dir = "output_data"
os.makedirs(output_dir, exist_ok=True)

# Sidebar Configuration & Mode Switcher
st.sidebar.header("Configuration")
mode = st.sidebar.radio("Select Analysis Mode:", ["Single Plan Audit", "Revision Delta Comparison (Diffing)"])

jurisdiction = st.sidebar.selectbox(
    "Select Governing Building Code Jurisdiction:",
    ["2021 PA UCC (Pennsylvania Uniform Construction Code)", "2021 International Building Code (IBC)"]
)

rules_path = "config/pennsylvania_ucc_2021.json"
if not os.path.exists(rules_path) and os.path.exists("rules/pa_ucc_2021_rules.json"):
    rules_path = "rules/pa_ucc_2021_rules.json"

json_output_path = os.path.join(output_dir, "plan_text.json")

if mode == "Single Plan Audit":
    uploaded_file = st.sidebar.file_uploader("Upload Architectural Drawing (PDF)", type=["pdf"], key="single")
    if uploaded_file is not None:
        target_pdf = os.path.join(output_dir, uploaded_file.name)
        with open(target_pdf, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")
    else:
        target_pdf = "sample_plan_A101.pdf"
        st.sidebar.info("Using default sample drawing: sample_plan_A101.pdf")

    try:
        parse_drawing_pdf(target_pdf, json_output_path, output_dir)
    except Exception as e:
        st.error(f"Error parsing PDF drawing: {e}")

else:
    st.sidebar.subheader("Upload Drawing Revisions")
    file_old = st.sidebar.file_uploader("1. Upload Original Drawing (PDF)", type=["pdf"], key="old")
    file_new = st.sidebar.file_uploader("2. Upload Revised Drawing (PDF)", type=["pdf"], key="new")
    st.sidebar.info("Diff Color Key:\n- 🟢 Green: Added Geometry\n- 🔴 Red: Removed Geometry\n- ⬛ Dark: Unchanged")

# Tabs Layout
tab1, tab2, tab3 = st.tabs(["📋 Compliance Audit Report", "🔍 Revision Visual Diff", "🧊 Interactive 3D Model"])

with tab1:
    st.header("Architectural Building Code Compliance Audit Report")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📐 Blueprint Preview")
        preview_img_path = os.path.join(output_dir, "sheet_page_1.png")
        if os.path.exists(preview_img_path):
            img = Image.open(preview_img_path)
            st.image(img, caption="Active Drawing Sheet A-101")
        else:
            st.warning("Blueprint preview image not generated yet.")

    with col2:
        run_audit = st.button("🚀 Run Full Compliance Audit")
        if run_audit:
            audit_report_path = os.path.join(output_dir, "audit_report.md")
            pdf_report_path = os.path.join(output_dir, "PA_UCC_Compliance_Report.pdf")
            try:
                run_compliance_audit(json_output_path, rules_path, audit_report_path)
                if os.path.exists(audit_report_path):
                    generate_pdf_report(audit_report_path, pdf_report_path)
                    with open(audit_report_path, "r") as f:
                        report_markdown = f.read()
                    st.success("Audit Complete!")
                    if os.path.exists(pdf_report_path):
                        with open(pdf_report_path, "rb") as pdf_file:
                            st.download_button(
                                label="📄 Download Official PDF Report",
                                data=pdf_file,
                                file_name="PA_UCC_Compliance_Report.pdf",
                                mime="application/pdf"
                            )
                    st.markdown(report_markdown)
                else:
                    st.error("Audit completed, but audit_report.md was not found.")
            except Exception as audit_err:
                st.error(f"Error running compliance audit: {audit_err}")
        else:
            st.info("Click **'🚀 Run Full Compliance Audit'** above to generate report.")

with tab2:
    st.header("🔍 Plan Revision Visual Diffing & Delta Overlay")
    if mode == "Revision Delta Comparison (Diffing)":
        if file_old and file_new:
            path_old = os.path.join(output_dir, "old_" + file_old.name)
            path_new = os.path.join(output_dir, "new_" + file_new.name)
            
            with open(path_old, "wb") as f: f.write(file_old.getbuffer())
            with open(path_new, "wb") as f: f.write(file_new.getbuffer())

            parse_drawing_pdf(path_old, os.path.join(output_dir, "old.json"), os.path.join(output_dir, "old_out"))
            parse_drawing_pdf(path_new, os.path.join(output_dir, "new.json"), os.path.join(output_dir, "new_out"))

            img_old_path = os.path.join(output_dir, "old_out", "sheet_page_1.png")
            img_new_path = os.path.join(output_dir, "new_out", "sheet_page_1.png")

            if os.path.exists(img_old_path) and os.path.exists(img_new_path):
                diff_path = generate_plan_diff(img_old_path, img_new_path, os.path.join(output_dir, "diff_result.png"))
                st.subheader("Visual Delta Highlights")
                st.image(diff_path, caption="🟢 Green = Additions | 🔴 Red = Deletions | ⬛ Dark = Unchanged")
            else:
                st.error("Failed to render preview images for comparison.")
        else:
            st.info("Please upload both Original and Revised PDF sets in the sidebar to generate a visual diff overlay.")
    else:
        st.info("Switch Analysis Mode in sidebar to **'Revision Delta Comparison (Diffing)'** to compare two drawing sets.")

with tab3:
    st.subheader("🧊 Interactive 3D Architectural Extrusion Viewer")
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 1, 1])
    with col_ctrl1:
        wall_height = st.slider("Adjust Story Height (Z-Axis Extrusion in feet)", min_value=2.0, max_value=8.0, value=3.2, step=0.2)
    with col_ctrl2:
        render_mode = st.selectbox("Render View Mode:", ["Textured Solid", "Compliance Heatmap", "Wireframe / Transparent"])

    dynamic_rooms, dynamic_openings = load_rooms_and_openings(json_output_path, default_height=wall_height)
    with col_ctrl3:
        obj_file_path = export_to_obj(dynamic_rooms, "output_data/building_model.obj", wall_height=wall_height)
        if os.path.exists(obj_file_path):
            with open(obj_file_path, "rb") as f:
                st.download_button(
                    label="💾 Export 3D .OBJ File",
                    data=f,
                    file_name="building_model.obj",
                    mime="model/obj"
                )

    fig_3d = generate_3d_building_model(
        rooms_data=dynamic_rooms, 
        openings_data=dynamic_openings, 
        wall_height=wall_height,
        render_mode=render_mode
    )
    st.plotly_chart(fig_3d)