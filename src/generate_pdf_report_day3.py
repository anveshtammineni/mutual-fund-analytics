import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define directories
REPORTS_DIR = r"D:\mutual-fund-analytics\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
PDF_PATH = os.path.join(REPORTS_DIR, "Day_3_EDA_Visualisation_Report.pdf")
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
            self.drawString(54, 750, "DAY 3 REPORT: EXPLORATORY DATA ANALYSIS (EDA)")
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
    # Margins: Left/Right 54 pt. Printable width: 504 pt.
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
        spaceBefore=15,
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
        spaceBefore=10,
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
    story.append(Paragraph("<b>Day 3 Report — Exploratory Data Analysis (EDA)</b>", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Metadata Block
    meta_data = [
        [Paragraph("<b>Intern Name:</b>", body_style), Paragraph("Anvesh Tammineni", body_style)],
        [Paragraph("<b>Report Date:</b>", body_style), Paragraph("June 28, 2026", body_style)],
        [Paragraph("<b>Git Repository:</b>", body_style), Paragraph("github.com/anveshtammineni/mutual-fund-analytics", body_style)],
        [Paragraph("<b>Commit Message:</b>", body_style), Paragraph("Day 3: Exploratory Data Analysis & Visualisation complete", body_style)],
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
        "This report delivers a visual, conformed Exploratory Data Analysis (EDA) of the mutual fund analytics database. "
        "The analysis explores daily NAV trajectories, Assets Under Management (AUM) scaling, monthly SIP trends, "
        "investor demographic profiles, geographical metrics, returns correlations, and equity portfolio sector weights. "
        "All visual charts are generated and exported directly from the conformed SQLite database (<code>bluestock_mf.db</code>) "
        "and clean data pipelines.",
        body_style
    ))
    story.append(Paragraph(
        "A total of 16 visualizations were constructed to expose underlying patterns and correlations. The following pages "
        "display the primary charts alongside corresponding business insights and findings.",
        body_style
    ))
    
    story.append(PageBreak())

    # ================= PAGES 2+: CHARTS & INSIGHTS =================
    
    # Helper function to add a chart and its insight
    def add_chart_block(title, image_name, width, height, insight_text):
        img_path = os.path.join(IMAGE_DIR, image_name)
        block = []
        block.append(Paragraph(title, h2_style))
        if os.path.exists(img_path):
            block.append(Spacer(1, 4))
            block.append(Image(img_path, width=width, height=height))
            block.append(Spacer(1, 8))
        else:
            block.append(Paragraph(f"<i>Error: Image {image_name} not found.</i>", body_style))
        block.append(Paragraph(f"<b>Business Insight:</b> {insight_text}", body_style))
        block.append(Spacer(1, 15))
        return block

    # We will fit 2 charts per page to keep it clean and elegant
    
    # Page 2: NAV Trends & AUM Growth
    story.extend(add_chart_block(
        "1. Daily NAV Trend Analysis (2022 - 2026)",
        "01_nav_trend_plotly.png",
        420, 210,
        "Daily NAV trend analysis reveals a strong upward trajectory across all 40 schemes during the 2023 market bull run (green region), "
        "followed by structural volatility and corrections in the first half of 2024 (red region)."
    ))
    story.extend(add_chart_block(
        "2. AUM Growth by Fund House (2022 - 2025)",
        "02_aum_growth_seaborn.png",
        420, 210,
        "AUM grouped bar chart shows that SBI Mutual Fund maintains a clear dominance in assets under management (AUM) "
        "compared to peer AMCs across all years (2022-2025), peaking at over ₹6.05 lakh crore."
    ))
    story.append(PageBreak())

    # Page 3: SIP Trends & Category Inflows
    story.extend(add_chart_block(
        "3. Monthly SIP Inflow Trend (2022 - 2025)",
        "03_sip_inflow_plotly.png",
        420, 210,
        "Monthly industry-wide SIP inflow trends show explosive growth, rising from ~₹11,517 Cr in Jan 2022 to an all-time record high "
        "of ₹31,002 Cr in December 2025."
    ))
    story.extend(add_chart_block(
        "4. Net Category Inflows Heatmap (2024 - 2025)",
        "04_category_inflow_heatmap.png",
        420, 210,
        "Heatmap analysis of category inflows demonstrates that Large Cap, Mid Cap, and Small Cap funds receive the most consistent "
        "positive net capital inflows, with occasional peaks in debt fund categories."
    ))
    story.append(PageBreak())

    # Page 4: Age & Ticket size distributions
    story.extend(add_chart_block(
        "5. Investor Age Group Distribution",
        "05_age_distribution_pie.png",
        300, 200,
        "Retail mutual fund participation is heavily skewed towards younger age brackets, with the 18–30 and 31–45 groups "
        "representing over 75% of the total investor base."
    ))
    story.extend(add_chart_block(
        "6. SIP Transaction Amount by Age Group",
        "06_sip_amount_by_age_box.png",
        400, 200,
        "SIP monthly installment sizes are relatively uniform across age groups, though the 31–45 age group has a slightly higher "
        "median investment amount, reflecting mature earning years."
    ))
    story.append(PageBreak())

    # Page 5: Gender & State Geography
    story.extend(add_chart_block(
        "7. Investor Gender Distribution",
        "07_gender_distribution_pie.png",
        300, 200,
        "Retail mutual fund participation is highly dominated by male investors (~74.8%), suggesting that targeted financial inclusion "
        "programs for women are highly needed."
    ))
    story.extend(add_chart_block(
        "8. Total SIP Investment Amount by State",
        "08_sip_amount_by_state_bar.png",
        400, 230,
        "Punjab, Tamil Nadu, and Madhya Pradesh stand out as the top three geographic contributors by total transaction values, "
        "reflecting strong retail investor presence in these regions."
    ))
    story.append(PageBreak())

    # Page 6: City Tier & Folio Growth
    story.extend(add_chart_block(
        "9. City Tier Distribution: T30 vs B30",
        "09_t30_b30_pie.png",
        300, 200,
        "City-tier analysis shows that the vast majority of retail mutual fund investors (over 70%) reside in Top 30 (T30) cities, "
        "while Beyond 30 (B30) cities represent a growing but still under-penetrated market segment."
    ))
    story.extend(add_chart_block(
        "10. Industry Folio Count Growth (2022 - 2025)",
        "10_folio_growth_line.png",
        400, 200,
        "The mutual fund industry's folio counts have experienced massive growth, doubling from 13.26 Cr in January 2022 to 26.12 Cr "
        "in December 2025, marking a period of massive retail onboarding."
    ))
    story.append(PageBreak())

    # Page 7: Return correlation & Sector allocations
    story.extend(add_chart_block(
        "11. Pairwise NAV Return Correlation Matrix",
        "11_return_correlation_heatmap.png",
        360, 240,
        "Returns correlation matrix for selected funds indicates high positive correlation among equity schemes, "
        "and low correlation between equity and debt schemes, illustrating standard diversification benefits."
    ))
    story.extend(add_chart_block(
        "12. Aggregate Sector Allocation across Equity Funds",
        "12_sector_allocation_donut.png",
        360, 240,
        "Sector allocation donut chart shows that Consumer Goods (avg weight 14.18%) and IT (11.39%) are the top heavily allocated sectors "
        "across equity portfolios, representing core holdings."
    ))
    story.append(PageBreak())

    # Page 8: Additional analysis distributions
    story.extend(add_chart_block(
        "13. Distribution of Investor Transaction Amounts",
        "13_transaction_amount_distribution.png",
        400, 180,
        "Investor transactions show a right-skewed distribution, with the majority of retail contributions under ₹10,000 INR, "
        "confirming that micro-investing via SIP is the dominant form of market participation."
    ))
    story.extend(add_chart_block(
        "14. Top 10 Stock Holdings by Aggregate Market Value",
        "14_top_stock_holdings_bar.png",
        400, 180,
        "Equity portfolios show high concentration in blue-chip holdings, with Axis Bank, Bharti Airtel, and Reliance Industries "
        "representing the top three stock allocations by aggregate market value."
    ))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>End of Day 3 Visualisation Report</b>", body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
