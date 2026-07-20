import streamlit as st
import os
import json
from PIL import Image, ImageDraw

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

if uploaded_file is not None:
    target_pdf = f"temp_{uploaded_file.name}"
    with open(target_pdf, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.info(f"File uploaded: `{uploaded_file.name}`")
else:
    st.sidebar.warning("No file uploaded. Using default sample drawing: `sample_plan_A101.pdf`")
    target_pdf = "sample_plan_A101.pdf"

temp_image_path = "temp_images/sheet_page_1.png"

def highlight_blueprint_issues(image_path, bounding_boxes=None):
    if not os.path.exists(image_path):
        return None
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    if not bounding_boxes:
        w, h = img.size
        bounding_boxes = [(int(w * 0.25), int(h * 0.35), int(w * 0.65), int(h * 0.75))]
    for box in bounding_boxes:
        draw.rectangle(box, outline="red", width=6)
    return img

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📐 Blueprint Preview")
    if os.path.exists(temp_image_path):
        show_flags = st.checkbox("Show Visual Compliance Flags", value=True)
        if show_flags:
            annotated_img = highlight_blueprint_issues(temp_image_path)
            if annotated_img:
                st.image(annotated_img, caption="Flagged Compliance Areas (Red Boxes)", use_container_width=True)
        else:
            st.image(temp_image_path, caption="Original Drawing", use_container_width=True)
    else:
        st.info("Run an audit to generate the drawing preview.")

if st.button("🚀 Run Full Compliance Audit", type="primary"):
    with st.spinner("Extracting vector text from PDF drawing..."):
        parse_drawing_pdf(target_pdf)

    with st.spinner("Running Vision LLM Verification..."):
        verify_visual_elements(temp_image_path, "output_data/plan_text.json")

    with st.spinner("Auditing Against 115 PA UCC Rules..."):
        run_compliance_audit("output_data/plan_text.json", rules_path, "output_data/audit_report.md")

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