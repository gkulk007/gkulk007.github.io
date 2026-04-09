import os
import json
from pdf2image import convert_from_path

# Root directory
ROOT_DIR = "certificates"
OUTPUT_JSON = os.path.join(ROOT_DIR, "certificates.json")

# Optional: Poppler path (Windows only)
POPPLER_PATH = r"Release-25.12.0-0\poppler-25.12.0\Library\bin"


def delete_existing_webp(folder):
    """Delete all existing WEBP files in a folder"""
    for file in os.listdir(folder):
        if file.lower().endswith(".webp"):
            os.remove(os.path.join(folder, file))
            print(f"🗑️ Deleted: {file}")


def convert_pdf_to_single_webp(pdf_path):
    """Convert only FIRST PAGE of PDF to WEBP"""
    try:
        print(f"📄 Processing: {pdf_path}")

        # Convert only first page
        images = convert_from_path(
            pdf_path,
            first_page=1,
            last_page=1,
            poppler_path=POPPLER_PATH
        )

        if not images:
            return None

        image = images[0]

        base_name = os.path.splitext(pdf_path)[0]
        webp_path = f"{base_name}.webp"

        image.save(webp_path, "WEBP", quality=85)

        print(f"✅ Created: {webp_path}")

        return os.path.basename(base_name)

    except Exception as e:
        print(f"❌ Error: {pdf_path} → {e}")
        return None


def process_all():
    data = {}

    for category in os.listdir(ROOT_DIR):
        category_path = os.path.join(ROOT_DIR, category)

        if not os.path.isdir(category_path):
            continue

        print(f"\n📁 Category: {category}")

        # Step 1: Clean old WEBP files
        delete_existing_webp(category_path)

        cert_list = []

        for file in os.listdir(category_path):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(category_path, file)

                base_name = convert_pdf_to_single_webp(pdf_path)

                if base_name:
                    cert_list.append(base_name)

        if cert_list:
            data[category] = sorted(cert_list)

    # Step 3: Write JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n📦 JSON updated: {OUTPUT_JSON}")


if __name__ == "__main__":
    process_all()