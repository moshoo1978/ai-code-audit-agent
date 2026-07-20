import streamlit as st
import os
import json
from scripts.parse_pdf import parse_drawing_pdf
from scripts.vision_verifier import verify_visual_elements
from scripts.run_audit import run_compliance_audit

st.set_page_config(page_title="AI Architectural Drawing Audit Agent", page_icon="🏛️", layout="wide")

st.title("🏛️ AI Architectural Drawing & Code Audit Agent")
st.markdown("**Automated PA UCC & Multi-Discipline Building Code Compliance Checker**")
st.divider()

# Sidebar Setup
st.sidebar.header("⚙️ Configuration")
rules_path = "config/pennsylvania_ucc_2021.json"

if os.path.exists(rules_path):
    with open(rules_path, "r") as f:
        rules_data = json.load(f)
    st.sidebar.success(f"Loaded {len(rules_data.get('rules', []))} PA UCC Rules")
    st.sidebar.caption(f"**Governing Code:**\n{rules_data.get('governing_code', 'PA UCC')}")

uploaded_file = st.sidebar.file_uploader("Upload Architectural Drawing (PDF)", type=["pdf"])

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Drawing Input & Processing")
    if uploaded_file is not None:
        save_path = f"temp_images/{uploaded_file.name}"
        os.makedirs("temp_images", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.info(f"File uploaded: `{uploaded_file.name}`")
        target_pdf = save_path
    else:
        st.warning("No file uploaded. Using default sample drawing: `sample_plan_A101.pdf`")
        target_pdf = "sample_plan_A101.pdf"

    if st.button("🚀 Run Full Compliance Audit", type="primary"):
        parsed_json_path = "output_data/plan_text.json"
        report_path = "output_data/audit_report.md"
        image_path = "temp_images/sheet_page_1.png"

        with st.spinner("Extracting PDF Vector Text & Rasterizing..."):
            parse_drawing_pdf(target_pdf, parsed_json_path, "temp_images")

        with st.spinner("Running Vision AI Geometry Verification..."):
            verify_visual_elements(image_path, parsed_json_path)

        with st.spinner("Auditing Against 115 PA UCC Rules..."):
            run_compliance_audit(parsed_json_path, rules_path, report_path)

        st.success("Audit Complete!")

with col2:
    st.subheader("📋 Compliance Audit Report")
    report_file = "output_data/audit_report.md"
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            report_text = f.read()
        st.markdown(report_text)

        st.divider()
        st.download_button(
            label="📥 Download Audit Report (.md)",
            data=report_text,
            file_name="PA_UCC_Building_Code_Audit_Report.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.info("Click **Run Full Compliance Audit** to generate the audit report.")
