import fitz  # PyMuPDF
import json
import os

def parse_drawing_pdf(pdf_path, output_json_path, image_output_dir):
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File {pdf_path} not found.")
        return

    os.makedirs(image_output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    
    extracted_data = {
        "file_name": os.path.basename(pdf_path),
        "total_pages": len(doc),
        "pages": []
    }

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 1. Render page to high-res 300 DPI PNG image for Vision AI
        pix = page.get_pixmap(dpi=300)
        image_filename = f"sheet_page_{page_num + 1}.png"
        image_path = os.path.join(image_output_dir, image_filename)
        pix.save(image_path)
        
        # 2. Extract plain text and structured bounding boxes
        plain_text = page.get_text("text").strip()
        text_page = page.get_text("dict")
        text_elements = []

        for block in text_page.get("blocks", []):
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text_elements.append({
                            "text": span["text"].strip(),
                            "bbox": [round(c, 2) for c in span["bbox"]],
                            "font_size": round(span["size"], 1)
                        })

        extracted_data["pages"].append({
            "page_number": page_num + 1,
            "image_path": image_path,
            "raw_text": plain_text,
            "text_elements": text_elements
        })

    doc.close()

    # Save updated JSON metadata
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    print(f"✅ Successfully extracted text JSON & high-res sheet image!")
    print(f"   📄 JSON Output:  {output_json_path}")
    print(f"   🖼️  Image Saved: {image_output_dir}/sheet_page_1.png")

if __name__ == "__main__":
    parse_drawing_pdf("sample_plan_A101.pdf", "output_data/plan_text.json", "temp_images")
