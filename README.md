# 🏛️ AI Architectural Drawing & Code Audit Agent

An automated, multi-discipline building code compliance checker powered by computer vision, vector extraction, and multi-agent AI pipelines. Built for the **2021 Pennsylvania Uniform Construction Code (PA UCC)** and the **2021 International Building Code (IBC)**.

---

## 🌟 Key Features

* **📄 Multi-Modal Drawing Extraction:** Extracts both vector metadata/text from architectural PDFs and visual layout features using Vision LLM capabilities.
* **🎯 Visual Compliance Flagging:** Automatically highlights flagged architectural issues with visual bounding boxes directly on the blueprint preview.
* **⚖️ Multi-Jurisdiction Code Support:** Interactive sidebar allowing real-time switching between **2021 PA UCC**, **2021 IBC**, and custom regional amendments.
* **📋 Rule Engine Evaluation:** Audits extracted drawing parameters against 100+ structural, egress, fire, accessibility, and architectural rules.
* **📥 Exportable Audit Reports:** Formats detailed compliance tables with code citations, failure rationales, and one-click `.md` report downloading.

---

## 🏗️ Architecture Overview

[Architectural PDF Drawing]
│
├──► Vector Text Extractor (PyMuPDF) ──► Structural Parameters
│
└──► Vision Verifier (Pillow / Vision LLM) ──► Visual Annotations & Flags
│
▼
[Multi-Agent Rule Engine]
│
▼
[Interactive Streamlit Dashboard]
(Report Generation & Download)

## 🚀 Quickstart Guide

### Prerequisites
* Python 3.10+
* macOS / Linux / Windows

### 1. Clone the Repository
```bash
git clone [https://github.com/moshoo1978/ai-code-audit-agent.git](https://github.com/moshoo1978/ai-code-audit-agent.git)
cd ai-code-audit-agent
### 2. Set up Virtual Environments & Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Launch the Application
Bash
python3 -m streamlit run app.py
Open your browser to http://localhost:8501 to use the dashboard!

📂 Project Structure

ai-code-audit-agent/
├── app.py                      # Main Streamlit Dashboard UI
├── config/
│   └── pennsylvania_ucc_2021.json # Rule definitions & code standards
├── output_data/                # Generated JSON extractions & audit reports
├── scripts/
│   ├── parse_pdf.py            # PDF parsing & vector text extraction
│   ├── run_audit.py            # Rule evaluation engine
│   └── vision_verifier.py      # Vision LLM visual element verifier
├── temp_images/                # Processed blueprint image preview files
└── requirements.txt            # Python dependencies

📜 License

Distributed under the MIT License. See LICENSE for more information.
