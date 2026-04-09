import os
from pdf2image import convert_from_path
from PIL import Image

# Root directory
ROOT_DIR = "certificates"

# Optional: set poppler path if needed (Windows only)
POPPLER_PATH = r"Release-25.12.0-0\poppler-25.12.0\Library\bin" # e.g., r"C:\poppler\Library\bin"

def convert_pdf_to_webp(pdf_path):
    try:
        print(f"Processing: {pdf_path}")
        
        # Convert PDF to images (one image per page)
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        
        base_name = os.path.splitext(pdf_path)[0]
        
        for i, image in enumerate(images):
            webp_path = f"{base_name}_page{i+1}.webp"
            
            # Save as WEBP
            image.save(webp_path, "WEBP", quality=85)
        
        print(f"✅ Converted: {pdf_path}")
    
    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")

def process_all_pdfs(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                convert_pdf_to_webp(pdf_path)

if __name__ == "__main__":
    process_all_pdfs(ROOT_DIR)