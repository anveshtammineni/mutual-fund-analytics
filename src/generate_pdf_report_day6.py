import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define directories
REPORTS_DIR = r"D:\mutual-fund-analytics\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
PDF_PATH = os.path.join(REPORTS_DIR, "Day_6_Advanced_Analytics_Report.pdf")
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
            self.drawString(54, 750, "DAY 6 REPORT: ADVANCED ANALYTICS & RISK METRICS")
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

    # ================= PAGE 1: TITLE & EXECUTIVE SUMMARY =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Bluestock Data Analyst Internship", subtitle_style))
    story.append(Paragraph("Capstone Project I: Mutual Fund Analytics", title_style))
    story.append(Paragraph("<b>Day 6 Report — Advanced Analytics & Risk Metrics</b>", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Metadata Block
    meta_data = [
        [Paragraph("<b>Intern Name:</b>", body_style), Paragraph("Anvesh Tammineni", body_style)],
        [Paragraph("<b>Report Date:</b>", body_style), Paragraph("July 2, 2026", body_style)],
        [Paragraph("<b>Git Repository:</b>", body_style), Paragraph("github.com/anveshtammineni/mutual-fund-analytics", body_style)],
        [Paragraph("<b>Commit Message:</b>", body_style), Paragraph("Day 6: Advanced Analytics & Risk Metrics complete", body_style)],
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
        "This report outlines the advanced risk analytics and customer behavior modeling performed on the conformed mutual fund database. "
        "Key deliverables include the Historical Value at Risk (VaR 95%) and Conditional Value at Risk (CVaR) boundaries, rolling Sharpe ratio trends, "
        "investor cohort structures, SIP gaps, and portfolio concentration indicators (HHI). "
        "Additionally, a standalone CLI recommender tool was constructed and verified.",
        body_style
    ))
    
    # Chart: Rolling Sharpe Ratio
    img_sharpe = os.path.join(IMAGE_DIR, "rolling_sharpe_chart.png")
    if os.path.exists(img_sharpe):
        story.append(Spacer(1, 10))
        story.append(Image(img_sharpe, width=420, height=210))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<i>Figure 1: Rolling 90-Day Sharpe Ratio trajectories across 5 key funds.</i>", table_cell_style))
    
    story.append(PageBreak())

    # ================= PAGE 2: VALUE AT RISK & INVESTOR COHORTS =================
    story.append(Paragraph("1. Value at Risk (VaR 95%) & CVaR Summary", h1_style))
    story.append(Paragraph(
        "The daily Value at Risk (95%) and Conditional Value at Risk (CVaR) were calculated for all 40 schemes. "
        "The results have been exported to <code>var_cvar_report.csv</code>. "
        "Equity funds display higher VaR/CVaR boundaries, with potential daily losses under extreme conditions exceeding 2.5%, "
        "while Gilt and Short Term Debt funds exhibit very low risk profiles (less than 1.1% daily VaR).",
        body_style
    ))
    
    story.append(Paragraph("2. Investor Cohort Analysis", h1_style))
    story.append(Paragraph(
        "Investors were grouped by the year of their first transaction. "
        "The analysis highlights that the 2025 cohort displays higher average monthly SIP tickets, "
        "reflecting increasing capital allocation per user over time:",
        body_style
    ))
    
    # Cohort Table
    headers = [
        Paragraph("Cohort Year", table_header_style),
        Paragraph("Avg SIP Amount (INR)", table_header_style),
        Paragraph("Total Invested (INR)", table_header_style),
        Paragraph("Top Preferred Fund", table_header_style)
    ]
    table_rows = [headers]
    
    cohort_data = [
        ("2024", "4,953.51", "1,770,250,000", "HDFC Mid-Cap Opportunities Fund"),
        ("2025", "5,119.78", "257,590,000", "ICICI Pru Bluechip Fund")
    ]
    
    for year, avg_sip, total_inv, top_pref in cohort_data:
        table_rows.append([
            Paragraph(year, table_cell_bold_style),
            Paragraph(avg_sip, table_cell_style),
            Paragraph(total_inv, table_cell_style),
            Paragraph(top_pref, table_cell_style)
        ])
        
    t_cohort = Table(table_rows, colWidths=[80, 120, 110, 194])
    t_cohort.setStyle(TableStyle([
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
    story.append(t_cohort)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("3. SIP Continuity & Churn Risk Analysis", h1_style))
    story.append(Paragraph(
        "A date gap analysis was performed on investors with 6 or more monthly SIP transactions. "
        "The overall industry SIP continuity adherence rate stands at <b>88.2%</b>. "
        "The remaining 11.8% of investors have average gaps between consecutive dates exceeding 35 days "
        "and are flagged as 'at-risk' of churn. This indicates minor mandate processing bottlenecks or customer liquidity shortfalls.",
        body_style
    ))
    
    story.append(PageBreak())

    # ================= PAGE 3: SECTOR HHI & RECOMMENDER =================
    story.append(Paragraph("4. Sector Herfindahl-Hirschman Index (HHI) Concentration", h1_style))
    story.append(Paragraph(
        "The sector concentration was evaluated using HHI ($\sum weight\_pct^2$) across all equity funds. "
        "A higher HHI indicates a concentrated thematic portfolio, while a lower HHI represents diversification:",
        body_style
    ))
    story.append(Paragraph("• <b>Highly Concentrated (HHI > 2500)</b>: Thematic and Sectoral funds (e.g. Technology, Infrastructure).", bullet_style))
    story.append(Paragraph("• <b>Moderately Concentrated (1500 to 2500)</b>: Core Large Cap and Mid Cap equity portfolios.", bullet_style))
    story.append(Paragraph("• <b>Diversified (HHI < 1500)</b>: Flexicap and Multicap funds (e.g. Kotak Flexicap HHI: 1,320).", bullet_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Interactive Recommender CLI Tool", h1_style))
    story.append(Paragraph(
        "A standalone command-line recommender script (<code>recommender.py</code>) was developed. "
        "It maps the user's risk profile (Low, Moderate, High) to fund categories, ranks them by Sharpe ratio, "
        "and returns the top 3 recommended schemes in a formatted CLI table:",
        body_style
    ))
    
    # Recommender table mock
    headers_rec = [
        Paragraph("Risk Profile", table_header_style), 
        Paragraph("Top Fund Recommendation", table_header_style), 
        Paragraph("Sharpe Ratio", table_header_style),
        Paragraph("3yr CAGR", table_header_style)
    ]
    rec_rows = [headers_rec]
    
    rec_data = [
        ("Low", "SBI Magnum Gilt Fund - Regular - Growth", "-0.74", "5.84%"),
        ("Moderate", "Mirae Asset Large Cap Fund - Regular - Growth", "1.07", "34.00%"),
        ("High", "Mirae Asset Tax Saver Fund - Regular - Growth", "0.92", "29.18%")
    ]
    
    for appetite, scheme, sharpe, cagr in rec_data:
        rec_rows.append([
            Paragraph(appetite, table_cell_bold_style),
            Paragraph(scheme, table_cell_style),
            Paragraph(sharpe, table_cell_style),
            Paragraph(cagr, table_cell_style)
        ])
        
    t_rec = Table(rec_rows, colWidths=[90, 240, 84, 90])
    t_rec.setStyle(TableStyle([
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
    story.append(t_rec)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>End of Day 6 Advanced Analytics Report</b>", body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
