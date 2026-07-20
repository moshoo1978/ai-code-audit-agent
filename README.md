# 🏛️ AI Architectural Drawing & Building Code Audit Agent

An end-to-end AI system for parsing architectural blueprint PDFs, performing visual geometry verification, and executing automated compliance audits against **115 multi-discipline codes** under the **Pennsylvania Uniform Construction Code (PA UCC)** framework.

## 🌟 Key Features
* **📄 PDF Vector Extraction & Rendering:** Converts blueprint PDFs into structured JSON data and high-res images.
* **👁️ Vision AI Geometry Verification:** Detects door swings, ADA turn clearances, and egress paths.
* **📜 115-Rule PA UCC Compliance Engine:** Covers 2021 IBC, IFC, IPC, IMC, IECC, IEBC, IFGC, ISPSC, IWUIC, ICCPC, 2020 NEC, NFPA 13/72/101, and PA statutory amendments.
* **💻 Interactive Web Dashboard:** Drag-and-drop PDF uploads and real-time report rendering via Streamlit.

## ⚙️ Quickstart
1. Run CLI Audit: `python3 main.py`
2. Launch Web Dashboard: `python3 -m streamlit run app.py`
