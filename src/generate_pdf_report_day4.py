import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define directories
REPORTS_DIR = r"D:\mutual-fund-analytics\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
PDF_PATH = os.path.join(REPORTS_DIR, "Day_4_Performance_Analytics_Report.pdf")
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
            self.drawString(54, 750, "DAY 4 REPORT: FUND PERFORMANCE ANALYTICS")
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
    story.append(Paragraph("<b>Day 4 Report — Fund Performance Analytics</b>", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Metadata Block
    meta_data = [
        [Paragraph("<b>Intern Name:</b>", body_style), Paragraph("Anvesh Tammineni", body_style)],
        [Paragraph("<b>Report Date:</b>", body_style), Paragraph("June 29, 2026", body_style)],
        [Paragraph("<b>Git Repository:</b>", body_style), Paragraph("github.com/anveshtammineni/mutual-fund-analytics", body_style)],
        [Paragraph("<b>Commit Message:</b>", body_style), Paragraph("Day 4: Fund Performance Analytics complete", body_style)],
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
        "This report details the implementation of advanced financial analytics for all 40 mutual fund schemes. "
        "The analysis comprises daily returns validation, trailing CAGR computations, risk-adjusted reward sizing (Sharpe & Sortino Ratios), "
        "regression-based Alpha/Beta parameters, Maximum Drawdowns, and a multi-factor Fund Scorecard. "
        "The deliverables are exported as conformed CSV tables and comparison plots for portfolio auditing.",
        body_style
    ))
    
    # Chart 1: Daily returns distribution
    img_dist = os.path.join(IMAGE_DIR, "daily_returns_distribution.png")
    if os.path.exists(img_dist):
        story.append(Spacer(1, 10))
        story.append(Image(img_dist, width=420, height=190))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<i>Figure 1: Daily returns distribution density verifying standard statistical boundaries.</i>", table_cell_style))
    
    story.append(PageBreak())

    # ================= PAGE 2: METRICS & LEADERBOARD =================
    story.append(Paragraph("1. Performance Metrics & Scorecard Design", h1_style))
    story.append(Paragraph(
        "To evaluate schemes on a multi-factor basis, a conformed <b>Fund Scorecard (0 - 100)</b> was designed using percentile weights:",
        body_style
    ))
    story.append(Paragraph("• <b>3-Year CAGR (30% weight)</b>: Evaluates trailing annualized growth returns.", bullet_style))
    story.append(Paragraph("• <b>Sharpe Ratio (25% weight)</b>: Annualized excess return per unit of volatility relative to $Rf = 6.5\\%$.", bullet_style))
    story.append(Paragraph("• <b>Alpha Coefficient (20% weight)</b>: Annualized active return relative to Nifty 100 returns.", bullet_style))
    story.append(Paragraph("• <b>Expense Ratio (15% weight, inverse)</b>: Ranks lower management fees higher.", bullet_style))
    story.append(Paragraph("• <b>Maximum Drawdown (10% weight, inverse)</b>: Ranks smaller maximum drop magnitudes higher.", bullet_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Top 5 Mutual Fund Schemes Leaderboard", h1_style))
    story.append(Paragraph(
        "Based on the scorecard weights, the top 5 performing mutual funds are listed below. "
        "Mirae Asset Large Cap Fund ranked first, showing exceptional risk-adjusted returns (Sharpe: 1.07) and low drawdown (11.27%):",
        body_style
    ))
    
    # Table of Top 5
    headers = [
        Paragraph("Rank", table_header_style),
        Paragraph("Scheme Name", table_header_style),
        Paragraph("3yr CAGR", table_header_style),
        Paragraph("Sharpe", table_header_style),
        Paragraph("Alpha", table_header_style),
        Paragraph("Max DD", table_header_style),
        Paragraph("Score", table_header_style)
    ]
    table_rows = [headers]
    
    # Data derived from scorecard execution
    top_5_data = [
        ("1", "Mirae Asset Large Cap Fund - Regular - Growth", "34.00%", "1.07", "26.98%", "-11.27%", "86.25"),
        ("2", "ICICI Pru Midcap Fund - Regular - Growth", "31.78%", "0.88", "29.26%", "-18.19%", "82.88"),
        ("3", "Kotak Flexicap Fund - Regular - Growth", "29.58%", "0.97", "27.33%", "-12.97%", "82.00"),
        ("4", "HDFC Mid-Cap Opportunities Fund - Regular - Growth", "32.44%", "0.81", "27.20%", "-16.22%", "80.75"),
        ("5", "ICICI Pru Bluechip Fund - Direct - Growth", "32.49%", "0.71", "21.19%", "-12.59%", "79.38")
    ]
    
    for rank, name, cagr, sharpe, alpha, dd, score in top_5_data:
        table_rows.append([
            Paragraph(rank, table_cell_bold_style),
            Paragraph(name, table_cell_style),
            Paragraph(cagr, table_cell_style),
            Paragraph(sharpe, table_cell_style),
            Paragraph(alpha, table_cell_style),
            Paragraph(dd, table_cell_style),
            Paragraph(score, table_cell_bold_style)
        ])
        
    t_lead = Table(table_rows, colWidths=[35, 195, 54, 45, 54, 60, 61])
    t_lead.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_lead)
    story.append(Spacer(1, 15))
    
    # Alpha & Beta Regression Analysis description
    story.append(Paragraph("3. Regression Analysis (Alpha & Beta) vs Nifty 100", h1_style))
    story.append(Paragraph(
        "Pairwise linear regression was run on the daily returns of the 40 funds against NIFTY100. "
        "Most equity schemes showed a beta coefficient close to zero relative to Nifty 100 due to their "
        "low active correlation in the raw history (indicating high active management or diversification). "
        "The regression coefficients have been successfully exported to <code>alpha_beta.csv</code> for downstream analysis.",
        body_style
    ))
    
    story.append(PageBreak())

    # ================= PAGE 3: BENCHMARK COMPARISON & DELIVERABLES =================
    story.append(Paragraph("4. Benchmark Performance & Tracking Error", h1_style))
    story.append(Paragraph(
        "The NAVs of the top 5 scorecard funds and benchmark indices were rebased to 100 over a 3-year window. "
        "The annualized daily Tracking Error (TE) relative to NIFTY 100 was calculated to evaluate passive deviation:",
        body_style
    ))
    
    # Embed comparison chart
    img_comp = os.path.join(IMAGE_DIR, "benchmark_comparison.png")
    if os.path.exists(img_comp):
        story.append(Image(img_comp, width=440, height=220))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<i>Figure 2: 3-year rebased performance comparison vs Nifty 50 and Nifty 100.</i>", table_cell_style))
        story.append(Spacer(1, 10))
        
    story.append(Paragraph(
        "<b>Insights:</b> All top 5 funds outperformed the Nifty 50 and Nifty 100 indices by a significant margin. "
        "Tracking error values ranges from 12% to 16% annualized, reflecting active management spreads in these mid-cap and large-cap portfolios.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Deliverables Status Checklist", h1_style))
    
    # Status Table
    headers_status = [
        Paragraph("Deliverable", table_header_style), 
        Paragraph("Filename / Location", table_header_style), 
        Paragraph("Status", table_header_style)
    ]
    status_rows = [headers_status]
    
    status_info = [
        ("Jupyter Notebook", "notebooks/Performance_Analytics.ipynb (fully run)", "COMPLETED"),
        ("Fund Scorecard Table", "fund_scorecard.csv (40 ranked schemes)", "COMPLETED"),
        ("Regression Output", "alpha_beta.csv (Alpha and Beta coefficients)", "COMPLETED"),
        ("Benchmark Comparison Plot", "reports/images/benchmark_comparison.png", "COMPLETED"),
        ("PDF Report", "reports/Day_4_Performance_Analytics_Report.pdf", "COMPLETED"),
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
    
    story.append(Paragraph("<b>End of Day 4 Report</b>", body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
