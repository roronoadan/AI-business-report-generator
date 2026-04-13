import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image, Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

os.makedirs("output/reports", exist_ok=True)

def generate_pdf(city: str, analysis: dict,
                 chart_paths: list) -> str:
    """Generate a professional PDF business intelligence report."""
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"output/reports/BI_Report_{city}_{date_str}.pdf"
    
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6, alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=12, textColor=colors.HexColor("#4a4a6a"),
        alignment=TA_CENTER, spaceAfter=4
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=14, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=16, spaceAfter=8,
        borderPad=4
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10.5, leading=16,
        textColor=colors.HexColor("#2d2d2d"),
        alignment=TA_JUSTIFY
    )
    
    story = []
    stats = analysis["stats"]
    
    # ── Header ──
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        f"Business Intelligence Report", title_style))
    story.append(Paragraph(
        f"{city} · Weather & Climate Analysis · "
        f"{datetime.now().strftime('%B %Y')}", subtitle_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(
        width="100%", thickness=2,
        color=colors.HexColor("#4a4a6a")))
    story.append(Spacer(1, 0.5*cm))
    
    # ── Key Metrics Table ──
    story.append(Paragraph("📊 Key Metrics", section_style))
    
    metrics_data = [
        ["Metric", "Value"],
        ["Average Temperature", f"{stats['avg_temp']} °C"],
        ["Maximum Temperature", f"{stats['max_temp']} °C"],
        ["Minimum Temperature", f"{stats['min_temp']} °C"],
        ["Total Precipitation", f"{stats['total_rain']} mm"],
        ["Rainy Days", f"{stats['rainy_days']} / 30 days"],
        ["Average Wind Speed", f"{stats['avg_wind']} km/h"],
        ["Temperature Trend", 
         f"{analysis['trend'].capitalize()} "
         f"(+{analysis['trend_delta']}°C)"],
    ]
    
    table = Table(metrics_data, colWidths=[9*cm, 7*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0),
         colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5,
         colors.HexColor("#cccccc")),
        ("PADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (1,0), (1,-1), "CENTER"),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5*cm))
    
    # ── AI Executive Summary ──
    story.append(Paragraph("🤖 AI Executive Summary", section_style))
    story.append(Paragraph(
        analysis["ai_summary"].replace("\n", "<br/>"), body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # ── Charts ──
    story.append(Paragraph("📈 Visual Analysis", section_style))
    
    chart_titles = [
        "Temperature Range Overview",
        "Daily Precipitation",
        "Wind Speed Trend",
        "Temperature Distribution"
    ]
    
    for i, (path, title) in enumerate(
            zip(chart_paths, chart_titles)):
        if os.path.exists(path):
            story.append(Paragraph(
                f"<b>{title}</b>",
                ParagraphStyle("ChartTitle",
                    parent=styles["Normal"],
                    fontSize=11, spaceAfter=6,
                    textColor=colors.HexColor("#4a4a6a"))
            ))
            story.append(Image(path, width=16*cm, height=6*cm))
            story.append(Spacer(1, 0.4*cm))
    
    # ── Footer ──
    story.append(HRFlowable(
        width="100%", thickness=1,
        color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"Generated automatically by AI Business Report Generator · "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')} · "
        f"github.com/roronoadan",
        ParagraphStyle("Footer", parent=styles["Normal"],
            fontSize=8, textColor=colors.gray,
            alignment=TA_CENTER)
    ))
    
    doc.build(story)
    print(f"✅ PDF Report saved: {filename}")
    return filename