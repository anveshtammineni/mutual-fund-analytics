import os
import glob
import shutil
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak
from reportlab.pdfgen import canvas

# Paths
ARTIFACT_DIR = r"C:\Users\anves\AppData\Local\Programs\Python\Python313\Lib\site-packages" # Wait, actually let's use the actual directory where artifacts are saved:
# The system told us: "Generated image is saved at C:\Users\anves\.gemini\antigravity\brain\9b4dd750-33d9-4f32-a637-6b087d614a35\dashboard_page_one_1782726715468.png"
CONV_DIR = r"C:\Users\anves\.gemini\antigravity\brain\9b4dd750-33d9-4f32-a637-6b087d614a35"
PROJECT_IMAGE_DIR = r"D:\mutual-fund-analytics\reports\images"
PDF_PATH = r"D:\mutual-fund-analytics\reports\Dashboard.pdf"

os.makedirs(PROJECT_IMAGE_DIR, exist_ok=True)

# Helper function to find and copy files
def copy_mockup_images():
    patterns = {
        "dashboard_page1.png": "dashboard_page_one_*.png",
        "dashboard_page2.png": "dashboard_page_two_*.png",
        "dashboard_page3.png": "dashboard_page_three_*.png",
        "dashboard_page4.png": "dashboard_page_four_*.png",
    }
    
    copied_files = []
    print("Searching for generated mockups in artifact directory...")
    for target_name, pattern in patterns.items():
        search_path = os.path.join(CONV_DIR, pattern)
        matching_files = glob.glob(search_path)
        
        if matching_files:
            # Sort to get the latest generated one
            latest_file = sorted(matching_files)[-1]
            dest_path = os.path.join(PROJECT_IMAGE_DIR, target_name)
            shutil.copy2(latest_file, dest_path)
            print(f"  - Copied {os.path.basename(latest_file)} -> reports/images/{target_name}")
            copied_files.append(dest_path)
        else:
            print(f"  - WARNING: No file found matching pattern {pattern}")
            
    return copied_files

def compile_pdf(image_paths):
    if not image_paths:
        print("ERROR: No images found to compile.")
        return
        
    print(f"Compiling dashboard pages into PDF: {PDF_PATH}")
    # Setup landscape letter document (792 width x 612 height)
    # Set margins to 0 so we can do full page dashboard layout
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(letter),
        leftMargin=10,
        rightMargin=10,
        topMargin=10,
        bottomMargin=10
    )
    
    story = []
    # Printable area: 792 - 20 = 772 width. Height: 612 - 20 = 592.
    # Standard dashboard 16:9 aspect ratio fits perfectly at 772 x 434, or we can use 750 x 422.
    for img_path in sorted(image_paths):
        story.append(Image(img_path, width=772, height=434))
        story.append(PageBreak())
        
    # Remove the last pagebreak to avoid empty page
    if story:
        story.pop()
        
    doc.build(story)
    print("Dashboard PDF compiled successfully.")

def main():
    copied = copy_mockup_images()
    compile_pdf(copied)

if __name__ == "__main__":
    main()
