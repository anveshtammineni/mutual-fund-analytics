import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define directories
REPORTS_DIR = r"D:\mutual-fund-analytics\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
PDF_PATH = os.path.join(REPORTS_DIR, "Day_2_Database_Design_Report.pdf")

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
            self.drawString(54, 750, "DAY 2 ETL REPORT: DATA CLEANING & DATABASE DESIGN")
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
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=12,
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
    story.append(Paragraph("<b>Day 2 Report — Data Cleaning + SQL Database Design</b>", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Metadata Block
    meta_data = [
        [Paragraph("<b>Intern Name:</b>", body_style), Paragraph("Anvesh Tammineni", body_style)],
        [Paragraph("<b>Report Date:</b>", body_style), Paragraph("June 24, 2026", body_style)],
        [Paragraph("<b>Git Repository:</b>", body_style), Paragraph("github.com/anveshtammineni/mutual-fund-analytics", body_style)],
        [Paragraph("<b>Commit Message:</b>", body_style), Paragraph("Day 2: Cleaned data + SQLite DB loaded", body_style)],
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
    
    # Section 1
    story.append(Paragraph("1. Data Cleaning Implementation", h1_style))
    story.append(Paragraph(
        "A robust Python ETL data cleaning script (<code>data_cleaning.py</code>) was developed using Pandas. "
        "The script processed all 10 datasets, loaded from raw storage, and written to processed directories under the following constraints:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>NAV History Expansion</b>: Parsed dates, dropped duplicates, and verified NAV > 0. "
        "By grouping by scheme and reindexing to daily frequency from minimum to maximum dates, we forward-filled (ffill) NAVs "
        "for weekends and holidays. This expanded `02_nav_history.csv` from 46,000 to 64,320 rows.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Transaction Standardization</b>: Standardized transactions into three types (`SIP`, `Lumpsum`, `Redemption`), "
        "validated transaction amounts > 0, set date formats, validated KYC status tags to a strict enum (`Verified`/`Pending`), and removed duplicates.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Performance Validation</b>: Coerced return figures to numeric values, used category-based medians to impute minor omissions, "
        "and enforced the expense ratio bounds between 0.1% and 2.5%.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Standard Cleaning (All Other Datasets)</b>: Standardized date formats, stripped leading/trailing spaces, "
        "deduplicated records, and outputted all 10 cleaned CSV files in <code>data/processed/</code>.",
        bullet_style
    ))
    
    story.append(PageBreak())

    # ================= PAGE 2: DB DESIGN & INGESTION VERIFICATION =================
    story.append(Paragraph("2. SQL Star Schema Database Design", h1_style))
    story.append(Paragraph(
        "A conformed relational Star Schema was modeled to optimize queries. A Python script (<code>db_loader.py</code>) "
        "created the SQLite database <code>bluestock_mf.db</code>, applied foreign key constraints (PRAGMA foreign_keys = ON), and loaded data. "
        "The schema design consists of the following conformed tables:",
        body_style
    ))
    story.append(Paragraph("• <b>dim_fund</b>: Primary dimension table containing scheme features, benchmark codes, and limits.", bullet_style))
    story.append(Paragraph("• <b>dim_date</b>: Shared date dimension, generated programmatically containing 1,608 unique dates, year, month, day, quarter, weekday, and weekend flag.", bullet_style))
    story.append(Paragraph("• <b>fact_nav</b>: Historical Net Asset Values over time (linked to fund and date dimensions).", bullet_style))
    story.append(Paragraph("• <b>fact_transactions</b>: Investor execution tracking, containing demographic details and amount values.", bullet_style))
    story.append(Paragraph("• <b>fact_performance</b>: Returns, ratings, volatility standard deviation, and drawdowns.", bullet_style))
    story.append(Paragraph("• <b>fact_aum</b>: AMC Assets Under Management over time.", bullet_style))
    story.append(Paragraph("• <b>Additional facts</b>: Tables for SIP Inflows, Category Net Inflows, Folios, Sector Holdings, and Indices.", bullet_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Ingestion Row-Count Verification", h1_style))
    story.append(Paragraph(
        "The database loader verified that every row from the cleaned source CSVs was loaded correctly. "
        "The comparison between CSV row counts and SQLite records shows complete parity:",
        body_style
    ))
    
    # Ingestion Audit Table
    headers = [
        Paragraph("SQLite Table Name", table_header_style), 
        Paragraph("Source Cleaned CSV File", table_header_style), 
        Paragraph("Record Count", table_header_style), 
        Paragraph("Status", table_header_style)
    ]
    table_rows = [headers]
    
    ingest_info = [
        ("dim_fund", "01_fund_master.csv", "40", "Match [OK]"),
        ("fact_nav", "02_nav_history.csv", "64,320", "Match [OK]"),
        ("fact_transactions", "08_investor_transactions.csv", "32,778", "Match [OK]"),
        ("fact_performance", "07_scheme_performance.csv", "40", "Match [OK]"),
        ("fact_aum", "03_aum_by_fund_house.csv", "90", "Match [OK]"),
        ("fact_sip_inflows", "04_monthly_sip_inflows.csv", "48", "Match [OK]"),
        ("fact_category_inflows", "05_category_inflows.csv", "144", "Match [OK]"),
        ("fact_industry_folios", "06_industry_folio_count.csv", "21", "Match [OK]"),
        ("fact_portfolio_holdings", "09_portfolio_holdings.csv", "322", "Match [OK]"),
        ("fact_benchmark_indices", "10_benchmark_indices.csv", "8,050", "Match [OK]"),
    ]
    
    for tbl, csv, count, status in ingest_info:
        table_rows.append([
            Paragraph(f"<code>{tbl}</code>", table_cell_bold_style),
            Paragraph(f"<code>{csv}</code>", table_cell_style),
            Paragraph(count, table_cell_style),
            Paragraph(status, table_cell_style)
        ])
        
    t_ingest = Table(table_rows, colWidths=[140, 180, 84, 100])
    t_ingest.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_ingest)
    
    story.append(PageBreak())

    # ================= PAGE 3: ANALYTICS & DELIVERABLES =================
    story.append(Paragraph("4. Analytical Queries & Reports Summary", h1_style))
    story.append(Paragraph(
        "Ten analytical SQL queries were coded in <code>queries.sql</code> and executed to generate metrics on the loaded database. "
        "Key analytical insights include:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Scheme AUM Leaderboard</b>: Mirae Asset Emerging Bluechip Fund is the largest equity fund in the database (AUM: 49,046 Cr), "
        "followed closely by Kotak Emerging Equity Fund (47,469 Cr).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>SIP YoY growth</b>: Growth percentage is missing for the first 12 months as expected. YoY calculations show a steady "
        "rise in overall industry inflows over time.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Geographical Revenue distribution</b>: Punjab (31.57 Cr) and Tamil Nadu (31.51 Cr) contributed the highest transaction volumes "
        "in Rupees, followed closely by Madhya Pradesh (30.83 Cr).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Low Expense Funds</b>: Nippon India Gilt Securities is the cheapest scheme (expense ratio: 0.55%), followed by "
        "HDFC Short Term Debt (0.56%).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Sector Holdings</b>: Consumer Goods (avg weight 14.18%) and IT (11.39%) are the top heavily allocated sectors. "
        "Axis Bank (16,325 Cr total value) is the most heavily held equity stock.",
        bullet_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Deliverables Checklist", h1_style))
    
    # Status Table
    headers_status = [
        Paragraph("Deliverable", table_header_style), 
        Paragraph("Location / Details", table_header_style), 
        Paragraph("Status", table_header_style)
    ]
    status_rows = [headers_status]
    
    status_info = [
        ("10 Cleaned CSVs", "data/processed/ (duplicates removed, forward-filled NAV)", "COMPLETED"),
        ("SQLite Database", "bluestock_mf.db (conformed star schema model)", "COMPLETED"),
        ("Schema DDL File", "schema.sql (auto-exported by loader script)", "COMPLETED"),
        ("Analytical Queries", "queries.sql (10 optimized SQL statements)", "COMPLETED"),
        ("Data Dictionary", "data_dictionary.md (table and column reference guide)", "COMPLETED"),
        ("Walkthrough Logs", "walkthrough.md (logs covering Day 1 + Day 2)", "COMPLETED"),
        ("PDF Report", "reports/Day_2_Database_Design_Report.pdf", "COMPLETED"),
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
    
    story.append(Paragraph("<b>End of Day 2 Report</b>", body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    doc_styles = getSampleStyleSheet()
    build_pdf()
