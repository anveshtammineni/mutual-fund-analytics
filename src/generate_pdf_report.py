import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define directories
REPORTS_DIR = r"D:\mutual-fund-analytics\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
PDF_PATH = os.path.join(REPORTS_DIR, "Day_1_Data_Ingestion_Report.pdf")

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
            self.drawString(54, 750, "DAY 1 ETL REPORT: MUTUAL FUND ANALYTICS")
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
    # Left and right margins: 54 pt (0.75 in), Top and bottom: 54 pt. Printable width: 504 pt.
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1A365D")   # Dark Navy
    c_secondary = colors.HexColor("#2B6CB0") # Teal/Blue
    c_dark = colors.HexColor("#2D3748")      # Charcoal Body Text
    c_light = colors.HexColor("#EDF2F7")     # Light Grey Background
    c_border = colors.HexColor("#E2E8F0")    # Border Line
    
    # Custom Typography Styles
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
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SubSecHeader',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
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
        leading=13.5,
        textColor=c_dark,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_dark
    )

    table_cell_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # ================= PAGE 1: TITLE & OVERVIEW =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Bluestock Data Analyst Internship", subtitle_style))
    story.append(Paragraph("Capstone Project I: Mutual Fund Analytics", title_style))
    story.append(Paragraph("<b>Day 1 Report — Project Setup + Data Ingestion (ETL)</b>", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Metadata Block
    meta_data = [
        [Paragraph("<b>Intern Name:</b>", body_style), Paragraph("Anvesh Tammineni", body_style)],
        [Paragraph("<b>Report Date:</b>", body_style), Paragraph("June 23, 2026", body_style)],
        [Paragraph("<b>Git Repository:</b>", body_style), Paragraph("github.com/anveshtammineni/mutual-fund-analytics", body_style)],
        [Paragraph("<b>Commit Message:</b>", body_style), Paragraph("Day 1: Data ingestion complete", body_style)],
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
    
    # Project Overview Section
    story.append(Paragraph("1. Project Overview & Repository Setup", h1_style))
    story.append(Paragraph(
        "This capstone project establishes a complete data analytics pipeline for mutual fund schemes in India. "
        "The first day focused on creating a standardized project folder layout, configuring environment dependencies, "
        "auditing the initial 10 datasets, validating relations, and retrieving real-time data from the official Open API (mfapi.in).",
        body_style
    ))
    story.append(Paragraph("The directory structure is organized as follows:", body_style))
    story.append(Paragraph("• <b>data/raw/</b>: Holds the 10 raw CSV datasets and newly fetched API CSVs.", bullet_style))
    story.append(Paragraph("• <b>src/</b>: Python execution scripts (<code>data_ingestion.py</code>, <code>live_nav_fetch.py</code>).", bullet_style))
    story.append(Paragraph("• <b>reports/</b>: Output summaries and generated PDF documentations.", bullet_style))
    story.append(Paragraph("• <b>requirements.txt</b>: Stores the package list and a concise data quality summary.", bullet_style))
    story.append(Spacer(1, 15))
    
    # Dependency Setup Section
    story.append(Paragraph("2. Dependency Installation", h1_style))
    story.append(Paragraph(
        "A reproducible environment was configured with package pinning. The main dependencies used include:",
        body_style
    ))
    story.append(Paragraph("• <b>pandas & numpy</b>: Core data analysis, clean structured loading, and manipulation.", bullet_style))
    story.append(Paragraph("• <b>matplotlib, seaborn & plotly</b>: Visualization libraries for subsequent dashboard features.", bullet_style))
    story.append(Paragraph("• <b>sqlalchemy</b>: Database connector interface for importing metrics to SQL databases.", bullet_style))
    story.append(Paragraph("• <b>requests</b>: Networking client library to query mfapi.in APIs.", bullet_style))
    story.append(Paragraph("• <b>scipy</b>: Analytical calculations and statistical metrics.", bullet_style))
    story.append(Paragraph("• <b>jupyter</b>: Interactive environments for draft analytics and investigations.", bullet_style))
    
    story.append(PageBreak())

    # ================= PAGE 2: DATA AUDIT & QUALITY SUMMARY =================
    story.append(Paragraph("3. Data Ingestion Audit", h1_style))
    story.append(Paragraph(
        "The script <code>data_ingestion.py</code> was executed to read all 10 raw CSV datasets using pandas. "
        "Each dataset was audited for shape (rows × columns), column data types, null counts, and duplicates. Below is the audited matrix:",
        body_style
    ))
    
    # Data Audit Table
    headers = [
        Paragraph("Filename", table_header_style), 
        Paragraph("Description", table_header_style), 
        Paragraph("Shape", table_header_style), 
        Paragraph("Null Values Found", table_header_style)
    ]
    
    table_rows = [headers]
    
    datasets_info = [
        ("01_fund_master.csv", "Fund Master", "40 x 15", "None"),
        ("02_nav_history.csv", "NAV History", "46,000 x 3", "None"),
        ("03_aum_by_fund_house.csv", "AUM by Fund House", "90 x 5", "None"),
        ("04_monthly_sip_inflows.csv", "Monthly SIP Inflows", "48 x 6", "12 (yoy_growth_pct)"),
        ("05_category_inflows.csv", "Category Inflows", "144 x 3", "None"),
        ("06_industry_folio_count.csv", "Industry Folio Count", "21 x 6", "None"),
        ("07_scheme_performance.csv", "Scheme Performance", "40 x 19", "None"),
        ("08_investor_transactions.csv", "Investor Transactions", "32,778 x 13", "None"),
        ("09_portfolio_holdings.csv", "Portfolio Holdings", "322 x 8", "None"),
        ("10_benchmark_indices.csv", "Benchmark Indices", "8,050 x 3", "None"),
    ]
    
    for filename, desc, shape, nulls in datasets_info:
        table_rows.append([
            Paragraph(f"<code>{filename}</code>", table_cell_bold_style),
            Paragraph(desc, table_cell_style),
            Paragraph(shape, table_cell_style),
            Paragraph(nulls, table_cell_style)
        ])
        
    t_audit = Table(table_rows, colWidths=[120, 160, 84, 140])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_audit)
    story.append(Spacer(1, 15))
    
    # Data Quality Analysis & Anomalies Section
    story.append(Paragraph("4. Data Quality & Anomalies Report", h1_style))
    story.append(Paragraph(
        "During audit, only one dataset presented missing values. In <b>04_monthly_sip_inflows.csv</b>, "
        "the column <code>yoy_growth_pct</code> contains 12 null records. An investigation confirmed that "
        "these nulls reside within the first 12 chronological rows of the dataset. Because the calculation of "
        "Year-over-Year (YoY) growth requires comparative data from the same month in the prior calendar year, "
        "no comparison baseline exists for the first year of entries. This is an expected mathematical limitation, "
        "rather than data corruption. No duplicates or unparseable dates were found across the other files.",
        body_style
    ))
    
    # Exploration & Code Validation
    story.append(Paragraph("5. Fund Master Exploration & AMFI Code Validation", h1_style))
    story.append(Paragraph(
        "A detailed search on <b>01_fund_master.csv</b> revealed that the database contains schemes "
        "distributed across 10 unique fund houses (e.g. SBI Mutual Fund, HDFC Mutual Fund, ICICI Prudential MF) "
        "spanning 2 core categories (Equity and Debt) and 12 distinct sub-categories (e.g. Large Cap, Mid Cap, Liquid, Gilt).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Validation Analysis:</b> Every AMFI code (numeric scheme identifier) present in "
        "<code>01_fund_master.csv</code> was verified against <code>02_nav_history.csv</code>. "
        "The script confirmed a <b>100% referential integrity match</b>: all 40 unique schemes "
        "defined in the Fund Master have corresponding historical NAV listings in the NAV History dataset.",
        body_style
    ))
    
    story.append(PageBreak())

    # ================= PAGE 3: API FETCHING & SUMMARY =================
    story.append(Paragraph("6. Live API NAV Integration", h1_style))
    story.append(Paragraph(
        "To ingestion live real-time metrics, the script <code>live_nav_fetch.py</code> was written "
        "to request recent data from the official endpoint <b>api.mfapi.in</b>. The results include:",
        body_style
    ))
    
    story.append(Paragraph("<b>A. HDFC Top 100 Direct Plan (AMFI Code: 125497)</b>", h2_style))
    story.append(Paragraph(
        "Successfully connected to the GET API and retrieved 3,105 rows. The data was parsed "
        "from the JSON response, and dates in the response (originally <code>DD-MM-YYYY</code> format) "
        "were converted to SQL-compliant standard <code>YYYY-MM-DD</code> format. The parsed records "
        "were written to <code>data/raw/live_hdfc_nav.csv</code>.",
        body_style
    ))
    
    story.append(Paragraph("<b>B. Key Schemes Verification (5 Major Mutual Funds)</b>", h2_style))
    story.append(Paragraph(
        "Historical and live NAV records were pulled for 5 major schemes to serve as our project benchmarks. "
        "The list includes:",
        body_style
    ))
    story.append(Paragraph("• <b>SBI Bluechip</b> (AMFI Code: 119551)", bullet_style))
    story.append(Paragraph("• <b>ICICI Bluechip</b> (AMFI Code: 120503)", bullet_style))
    story.append(Paragraph("• <b>Nippon Large Cap</b> (AMFI Code: 118632)", bullet_style))
    story.append(Paragraph("• <b>Axis Bluechip</b> (AMFI Code: 119092)", bullet_style))
    story.append(Paragraph("• <b>Kotak Bluechip</b> (AMFI Code: 120841)", bullet_style))
    
    story.append(Paragraph(
        "The response was parsed, aggregated, and compiled into a single unified dataset, "
        "comprising <b>16,777 combined records</b>, saved under <code>data/raw/key_schemes_nav.csv</code> "
        "with correct date formatting.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Deliverables & Verification
    story.append(Paragraph("7. Deliverables & Validation Status", h1_style))
    story.append(Paragraph(
        "All requested Day 1 deliverables have been verified, locally executed, and pushed to your remote repository:",
        body_style
    ))
    
    # Status Table
    headers_status = [
        Paragraph("Deliverable", table_header_style), 
        Paragraph("Filename / Location", table_header_style), 
        Paragraph("Status", table_header_style)
    ]
    status_rows = [headers_status]
    
    status_info = [
        ("Directory Structure", "data/raw, processed, src, reports, notebooks, sql", "COMPLETED"),
        ("Dependencies list", "requirements.txt (with Data Quality summary)", "COMPLETED"),
        ("Ingestion & Exploration", "src/data_ingestion.py", "COMPLETED"),
        ("Live API NAV Loader", "src/live_nav_fetch.py", "COMPLETED"),
        ("Data Quality Summary", "reports/data_quality_summary.md", "COMPLETED"),
        ("Ingestion & API Data", "data/raw/live_hdfc_nav.csv & key_schemes_nav.csv", "COMPLETED"),
        ("Version Control Push", "GitHub Repository (Day 1 Commit)", "COMPLETED"),
    ]
    
    for deliv, loc, status in status_info:
        status_rows.append([
            Paragraph(deliv, table_cell_bold_style),
            Paragraph(f"<code>{loc}</code>", table_cell_style),
            Paragraph(f"<b>{status}</b>", table_cell_style)
        ])
        
    t_status = Table(status_rows, colWidths=[130, 250, 124])
    t_status.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_status)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>End of Day 1 Report</b>", body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
