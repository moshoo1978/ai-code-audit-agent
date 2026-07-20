import os
import sys
from scripts.parse_pdf import parse_drawing_pdf
from scripts.vision_verifier import verify_visual_elements
from scripts.run_audit import run_compliance_audit

def main():
    print("\n" + "="*60)
    print(" 🏛️  AI ARCHITECTURAL DRAWING & CODE AUDIT AGENT ")
    print("="*60 + "\n")
    pdf_path = "sample_plan_A101.pdf"
    rules_path = "config/pennsylvania_ucc_2021.json"
    parsed_json_path = "output_data/plan_text.json"
    report_path = "output_data/audit_report.md"
    image_path = "temp_images/sheet_page_1.png"
    print("➡️ [1/3] Parsing Blueprint Vector Text & Raster Data...")
    parse_drawing_pdf(pdf_path, parsed_json_path, "temp_images")
    print("\n➡️ [2/3] Running Vision AI Verification...")
    verify_visual_elements(image_path, parsed_json_path)
    print("\n➡️ [3/3] Auditing Against PA UCC / 2021 IBC Rules...")
    run_compliance_audit(parsed_json_path, rules_path, report_path)
    print("\n" + "="*60)
    print("🎉 FULL AUDIT COMPLETE! Check output report at:")
    print("   " + report_path)
    print("="*60 + "\n")
if __name__ == "__main__":
    main()
