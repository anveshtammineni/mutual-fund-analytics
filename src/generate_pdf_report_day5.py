import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define directories
REPORTS_DIR = r"D:\mutual-fund-analytics\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
PDF_PATH = os.path.join(REPORTS_DIR, "Day_5_Dashboard_Development_Report.pdf")
IMAGE_DIR = os.path.join(REPORTS_DIR, "images")

# Custom Canvas for Page Numbers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        self.saveState()
        
        # Header (Only on page 2 and later)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1A365D"))
            self.drawString(54, 750, "DAY 5 REPORT: DASHBOARD DEVELOPMENT")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 55, 558, 55)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(54, 40, "Bluestock Data Analyst Internship — Capstone Project")
        
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        
        self.restoreState()

def build_pdf():
    # Page setup - letter size is 612 x 792 pt. 
    # Left and right margins: 54 pt. Printable width: 504 pt.
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Colors
    c_primary = colors.HexColor("#1A365D")   # Dark Navy
    c_secondary = colors.HexColor("#2B6CB0") # Teal/Blue
    c_dark = colors.HexColor("#2D3748")      # Charcoal Body Text
    c_light = colors.HexColor("#EDF2F7")     # Light Grey Background
    c_border = colors.HexColor("#E2E8F0")    # Border Line
    
    # Text Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'SecHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SubSecHeader',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        spaceAfter=10
    )

    story = []

    # ================= PAGE 1: TITLE & EXECUTIVE SUMMARY =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Bluestock Data Analyst Internship", subtitle_style))
    story.append(Paragraph("Capstone Project I: Mutual Fund Analytics", title_style))
    story.append(Paragraph("<b>Day 5 Report — Dashboard Development (Power BI)</b>", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Metadata Block
    meta_data = [
        [Paragraph("<b>Intern Name:</b>", body_style), Paragraph("Anvesh Tammineni", body_style)],
        [Paragraph("<b>Report Date:</b>", body_style), Paragraph("June 29, 2026", body_style)],
        [Paragraph("<b>Git Repository:</b>", body_style), Paragraph("github.com/anveshtammineni/mutual-fund-analytics", body_style)],
        [Paragraph("<b>Commit Message:</b>", body_style), Paragraph("Day 5: Dashboard Development & Power BI assets complete", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[100, 404])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 25))
    
    # Executive Summary Section
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "This report summarizes the design, visual layout, and configurations of the Power BI dashboard built for "
        "Mutual Fund Analytics. The dashboard is structured into 4 interactive reports to deliver clean, conformed business insights. "
        "Each page layout is detailed on the subsequent pages, showing the visual elements, key metrics, and design themes.",
        body_style
    ))
    story.append(Paragraph(
        "A multi-page conformed PDF document (<code>reports/Dashboard.pdf</code>) containing all landscape pages "
        "and a setup guide (<code>reports/PowerBI_Setup_Guide.md</code>) have been successfully compiled in the workspace.",
        body_style
    ))
    
    story.append(PageBreak())

    # ================= PAGES 2+: DASHBOARD PAGES & DESCRIPTIONS =================
    
    # Helper function to add a dashboard page and its description
    def add_page_block(title, image_name, desc_text):
        img_path = os.path.join(IMAGE_DIR, image_name)
        block = []
        block.append(Paragraph(title, h2_style))
        if os.path.exists(img_path):
            block.append(Spacer(1, 4))
            block.append(Image(img_path, width=440, height=247)) # fits nicely on letter page
            block.append(Spacer(1, 8))
        else:
            block.append(Paragraph(f"<i>Error: Image {image_name} not found.</i>", body_style))
        block.append(Paragraph(f"<b>Visual Elements & Insights:</b> {desc_text}", body_style))
        block.append(Spacer(1, 15))
        return block

    # Page 2: Page 1 - Industry Overview
    story.extend(add_page_block(
        "Page 1: Industry Overview",
        "dashboard_page1.png",
        "Displays corporate KPI cards showing Total AUM of ₹81L Crore, SIP Inflows of ₹31K Crore, Folios of 26.12 Crore, and 1,908 active schemes. "
        "A historical line chart documents the growth of industry AUM from 2022 to 2025, alongside a bar chart ranking the top AMCs (SBI, HDFC, ICICI) "
        "by total assets under management."
    ))
    story.append(PageBreak())

    # Page 3: Page 2 - Fund Performance
    story.extend(add_page_block(
        "Page 2: Fund Performance",
        "dashboard_page2.png",
        "Features a scatter plot evaluating annualized daily return (X-axis) against annualized daily risk (Y-axis), "
        "with bubble size indicating AUM level. A sortable scorecard table presents compound returns, Sharpe/Sortino ratios, and Alphas. "
        "It supports interactive category slicers and details drill-through."
    ))
    story.append(PageBreak())

    # Page 4: Page 3 - Investor Analytics
    story.extend(add_page_block(
        "Page 3: Investor Analytics",
        "dashboard_page3.png",
        "Outlines investor participation by geography and age. Displays transaction values ranked by state (Punjab, Tamil Nadu, and Madhya Pradesh leading), "
        "a donut chart of transaction type splits (SIP vs. Lumpsum vs. Redemption), and average monthly SIP amounts across age brackets. "
        "Supports tier and state slicers."
    ))
    story.append(PageBreak())

    # Page 5: Page 4 - SIP & Market Trends
    story.extend(add_page_block(
        "Page 4: SIP & Market Trends",
        "dashboard_page4.png",
        "Illustrates market indicators by comparing monthly SIP inflows (bars) against Nifty 50 close price (line) to explore correlations. "
        "A matrix heatmap visualizes monthly inflows across 10 scheme categories, highlighting the peak interest in Small Cap and Flexi Cap schemes."
    ))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>End of Day 5 Dashboard Development Report</b>", body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
