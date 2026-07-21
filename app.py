from scripts.generator_3d import generate_3d_building_model
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

# Sidebar Setup & Multi-Jurisdiction Code Selector
st.sidebar.header("⚙️ Configuration")

jurisdiction = st.sidebar.selectbox(
    "Select Governing Building Code Jurisdiction:",
    [
        "2021 PA UCC (Pennsylvania Uniform Construction Code)",
        "2021 IBC (International Building Code Standard)",
        "Custom Regional Code Amendments"
    ]
)

# Map jurisdiction choice to rule configuration file
if "PA UCC" in jurisdiction:
    rules_path = "config/pennsylvania_ucc_2021.json"
elif "IBC" in jurisdiction:
    rules_path = "config/ibc_2021.json" if os.path.exists("config/ibc_2021.json") else "config/pennsylvania_ucc_2021.json"
else:
    rules_path = "config/pennsylvania_ucc_2021.json"

if os.path.exists(rules_path):
    with open(rules_path, "r") as f:
        rules_data = json.load(f)
    st.sidebar.success(f"Loaded {len(rules_data.get('rules', []))} Rules")
    st.sidebar.caption(f"**Active Code Standard:**\n{jurisdiction}")

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

    with st.spinner(f"Auditing Against {jurisdiction}..."):
        run_compliance_audit("output_data/plan_text.json", rules_path, "output_data/audit_report.md")

    st.success("Audit Complete!")

with col2:
    tab1, tab2 = st.tabs(["📋 Compliance Audit Report", "🧊 Interactive 3D Model"])

with tab1:
    # --- PASTE YOUR EXISTING 2D REPORT DISPLAY CODE HERE ---
    st.header("Architectural Building Code Compliance Audit Report")


with tab2:
    st.subheader("🧊 3D Architectural Extrusion Viewer")
    st.info("💡 Tip: Click and drag with your mouse to rotate, zoom, and pan around the 3D structure.")
    
    wall_height = st.slider("Adjust Wall Height (Z-Axis Extrusion)", min_value=2.0, max_value=6.0, value=3.2, step=0.2)
    
    sample_rooms = [
        {"name": "OFFICE-101", "x": [0, 10, 10, 0, 0], "y": [0, 0, 8, 8, 0], "height": wall_height, "wall_color": "#1f77b4"},
        {"name": "Egress Corridor", "x": [10, 15, 15, 10, 10], "y": [0, 0, 8, 8, 0], "height": wall_height, "wall_color": "#ff7f0e"}
    ]
    
    fig_3d = generate_3d_building_model(sample_rooms)
    st.plotly_chart(fig_3d, use_container_width=True)