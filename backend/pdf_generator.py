"""
PDF Report Generator
Creates Arabic PDF reports for inspection results
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from datetime import datetime
import os
from typing import Dict, Any
import arabic_reshaper
from bidi.algorithm import get_display


async def generate_inspection_report(results: Dict[str, Any], inspection_id: str) -> str:
    """
    Generate PDF inspection report
    Returns path to generated PDF
    """
    report_dir = "../reports"
    os.makedirs(report_dir, exist_ok=True)
    
    pdf_filename = f"inspection_report_{inspection_id}.pdf"
    pdf_path = os.path.join(report_dir, pdf_filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Build content
    story = []
    styles = getSampleStyleSheet()
    
    # Arabic style
    arabic_style = ParagraphStyle(
        'Arabic',
        parent=styles['Normal'],
        alignment=TA_RIGHT,
        fontSize=12,
        leading=18
    )
    
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=18,
        leading=24,
        textColor=colors.HexColor('#00695C')
    )
    
    # Helper function for Arabic text
    def arabic_text(text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    
    # Title
    title = Paragraph(arabic_text("تقرير الفحص الذكي للمنشأة"), title_style)
    story.append(title)
    story.append(Spacer(1, 0.5*cm))
    
    # Subtitle
    subtitle = Paragraph(arabic_text("وزارة البلديات والإسكان - المملكة العربية السعودية"), arabic_style)
    story.append(subtitle)
    story.append(Spacer(1, cm))
    
    # Restaurant Info
    info_data = [
        [arabic_text("اسم المنشأة:"), results.get("restaurant_name", "غير محدد")],
        [arabic_text("رقم السجل التجاري:"), results.get("commercial_register", "غير محدد")],
        [arabic_text("رقم الفحص:"), inspection_id],
        [arabic_text("تاريخ الفحص:"), datetime.fromisoformat(results["timestamp"]).strftime("%Y-%m-%d %H:%M")],
    ]
    
    info_table = Table(info_data, colWidths=[6*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E0F2F1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, cm))
    
    # Overall Result
    status_ar = {
        "compliant": "مستوفي للمعايير",
        "needs_improvement": "يحتاج تحسينات",
        "non_compliant": "غير مستوفي"
    }
    
    status_color = {
        "compliant": colors.green,
        "needs_improvement": colors.orange,
        "non_compliant": colors.red
    }
    
    overall_status = results.get("overall_status", "non_compliant")
    score = results.get("overall_score", 0)
    
    result_data = [
        [arabic_text("النتيجة الإجمالية:"), arabic_text(status_ar[overall_status])],
        [arabic_text("الدرجة:"), f"{score:.1f}/100"],
    ]
    
    result_table = Table(result_data, colWidths=[6*cm, 10*cm])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), status_color[overall_status]),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(result_table)
    story.append(Spacer(1, cm))
    
    # Criteria Details
    criteria_title = Paragraph(arabic_text("تفاصيل المعايير"), title_style)
    story.append(criteria_title)
    story.append(Spacer(1, 0.5*cm))
    
    for criterion in results.get("criteria", []):
        crit_status = criterion.get("status", "non_compliant")
        crit_score = criterion.get("score", 0)
        crit_name = criterion.get("criterion_name", "")
        
        crit_data = [
            [arabic_text(crit_name), f"{crit_score}/100", arabic_text(status_ar[crit_status])]
        ]
        
        crit_table = Table(crit_data, colWidths=[10*cm, 3*cm, 3*cm])
        crit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ('TEXTCOLOR', (2, 0), (2, -1), status_color[crit_status]),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(crit_table)
        story.append(Spacer(1, 0.3*cm))
    
    story.append(Spacer(1, cm))
    
    # Footer
    footer = Paragraph(arabic_text("تم إنشاء هذا التقرير بواسطة نظام الفحص الذكي - وزارة البلديات والإسكان"), arabic_style)
    story.append(footer)
    
    # Build PDF
    doc.build(story)
    
    return pdf_path
