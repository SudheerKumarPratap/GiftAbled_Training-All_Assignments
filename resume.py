import io
import json
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import nest_asyncio

app = FastAPI(title="Decoupled Resume Generator Engine")

# 1. Pydantic validation schema matching your data models
class ResumeData(BaseModel):
    full_name: str
    email: str
    phone: str
    eduation:str
    professional_Summary: str
    experience: str
    skills: str

# 2. Function to dynamically read your configuration settings
def load_styling_config():
    config_path = "styles.css"
    if not os.path.exists(config_path):
        raise FileNotFoundError("Configuration file 'styles.css' missing from folder context.")
    with open(config_path, "r") as f:
        return json.load(f)

# 3. Dynamic PDF Generation Route Endpoint
@app.post("/generate-resume", tags=["Resume"])
def generate_pdf_resume(data: ResumeData):
    try:
        cfg = load_styling_config()
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Configuration Parsing Failure: {str(err)}")

    # Extract styling properties from the configuration dict arrays
    theme = cfg["theme"]
    typo = cfg["typography"]
    margins = cfg["margins"]

    buffer = io.BytesIO()
    
    # Establish structural padding template limits dynamically
    padding = margins["page_padding"]
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        leftMargin=padding, 
        rightMargin=padding, 
        topMargin=padding, 
        bottomMargin=padding
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Construct paragraph styles using your external styling variables
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName=typo["font_family"],
        fontSize=typo["title_size"],
        leading=int(typo["title_size"] * typo["line_spacing_ratio"]),
        textColor=colors.HexColor(theme["primary_color"]),
        alignment=1
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName=typo["font_family"],
        fontSize=typo["body_size"],
        leading=int(typo["body_size"] * typo["line_spacing_ratio"]),
        textColor=colors.HexColor(theme["text_muted"]),
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'DocSection',
        parent=styles['Heading2'],
        fontName=typo["font_family"],
        fontSize=typo["heading_size"],
        leading=int(typo["heading_size"] * typo["line_spacing_ratio"]),
        textColor=colors.HexColor(theme["secondary_color"]),
        spaceBefore=margins["section_gap"],
        spaceAfter=margins["item_gap"]
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName=typo["font_family"],
        fontSize=typo["body_size"],
        leading=int(typo["body_size"] * typo["line_spacing_ratio"]),
        textColor=colors.HexColor(theme["text_dark"])
    )

    # 4. Construct content nodes sequentially
    story.append(Paragraph(data.full_name, title_style))
    story.append(Paragraph(f"{data.email}  |  {data.phone}", contact_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Professional Summary", heading_style))
    story.append(Paragraph(data.professional_Summary, body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Work Experience", heading_style))
    story.append(Paragraph(data.experience.replace("\n", "<br/>"), body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Skills", heading_style))
    story.append(Paragraph(data.skills, body_style))
    
    # Render file content streams out to user context
    doc.build(story)
    buffer.seek(0)
    
    filename_clean = data.full_name.replace(' ', '_')
    return StreamingResponse(
        buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename={filename_clean}_Resume.pdf"}
    )

nest_asyncio.apply()

if __name__ == "__main__":
    uvicorn.run("resume:app", host="127.0.0.1", port=9000, reload=False)



