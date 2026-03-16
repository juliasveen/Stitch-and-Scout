from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import io
import datetime

MAROON   = colors.HexColor("#802b2b")
SAGE     = colors.HexColor("#b5c99a")
CREAM    = colors.HexColor("#fdfaf0")
TAN      = colors.HexColor("#d4a373")

COND_COLORS = {
    "New with Tags": colors.HexColor("#b5c99a"),
    "Like New":      colors.HexColor("#ffb7b2"),
    "Gently Used":   colors.HexColor("#d4a373"),
    "Well-Loved":    colors.HexColor("#802b2b"),
}

def generate_tag_pdf(
    item_name: str,
    item_type: str,
    price: float,
    condition: str,
    cost_paid: float = 0.0,
    platform: str = "",
    notes: str = "",
) -> bytes:
    """
    Generates a printable hang-tag PDF (A6 size).
    Returns raw PDF bytes for st.download_button.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A6,
        leftMargin=12*mm,
        rightMargin=12*mm,
        topMargin=16*mm,
        bottomMargin=12*mm,
    )

    cond_color  = COND_COLORS.get(condition, MAROON)
    profit      = price - cost_paid
    roi         = (profit / cost_paid * 100) if cost_paid > 0 else None

    # --- Styles ---
    title_style = ParagraphStyle("title",
        fontName="Helvetica-Bold", fontSize=20,
        textColor=MAROON, alignment=TA_CENTER, spaceAfter=2)

    sub_style = ParagraphStyle("sub",
        fontName="Helvetica-Oblique", fontSize=10,
        textColor=colors.HexColor("#5d1a1a"), alignment=TA_CENTER, spaceAfter=4)

    price_style = ParagraphStyle("price",
        fontName="Helvetica-Bold", fontSize=36,
        textColor=MAROON, alignment=TA_CENTER, spaceAfter=6)

    badge_style = ParagraphStyle("badge",
        fontName="Helvetica-Bold", fontSize=8,
        textColor=colors.white, alignment=TA_CENTER,
        backColor=cond_color, borderPadding=(3, 8, 3, 8),
        spaceAfter=8)

    meta_style = ParagraphStyle("meta",
        fontName="Helvetica", fontSize=8,
        textColor=colors.HexColor("#5d1a1a"), alignment=TA_CENTER, spaceAfter=3)

    profit_style = ParagraphStyle("profit",
        fontName="Helvetica-Bold", fontSize=9,
        textColor=colors.HexColor("#3b6d11") if profit >= 0 else MAROON,
        alignment=TA_CENTER, spaceAfter=2)

    note_style = ParagraphStyle("note",
        fontName="Helvetica-Oblique", fontSize=7,
        textColor=colors.HexColor("#888"), alignment=TA_CENTER)

    # --- Content ---
    story = []
    story.append(Paragraph(condition.upper(), badge_style))
    story.append(Paragraph(item_name.upper(), title_style))
    story.append(Paragraph(item_type, sub_style))
    story.append(HRFlowable(width="100%", thickness=1, lineCap="round",
                             color=MAROON, dash=(3, 3), spaceAfter=8))
    story.append(Paragraph(f"${price:.2f}", price_style))

    if platform:
        story.append(Paragraph(platform, meta_style))

    if cost_paid > 0:
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="80%", thickness=0.5, color=TAN, spaceAfter=6))
        story.append(Paragraph(f"Paid: ${cost_paid:.2f}", meta_style))
        roi_text = f"  |  ROI: {roi:.0f}%" if roi is not None else ""
        story.append(Paragraph(
            f"Est. profit: ${profit:.2f}{roi_text}", profit_style))

    if notes:
        story.append(Spacer(1, 6))
        story.append(Paragraph(notes[:120], note_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f"Stitch &amp; Scout · {datetime.date.today().strftime('%b %d, %Y')}",
        note_style))

    doc.build(story)
    return buffer.getvalue()