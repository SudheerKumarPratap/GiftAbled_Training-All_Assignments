
import uvicorn
import io,uvicorn
import re
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse

# ReportLab components
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI(title="Professional Resume Generator API")

def build_pdf_stream(
    name: str,
    phone: str,
    email: str,
    summary: str,
    qualification: str,
    experience: str,
    skills: str,
    projects :str,
    research_works :str,
    image_bytes: Optional[bytes] = None
) -> io.BytesIO:
    
    # 1. Initialize Memory Buffer
    buffer = io.BytesIO()
    
    # 2. Page Geometry & Document Setup (40pt margins for a crisp print bounds grid)
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        leftMargin=40, 
        rightMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    story = []
    
    # 3. Typography Styles Definition Setup
    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    PRIMARY_COLOR = colors.HexColor("#1A365D")   # Deep Corporate Navy
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") # Mid Slate Blue
    TEXT_COLOR = colors.HexColor("#2D3748")      # Soft Charcoal Body Text
    MUTED_TEXT = colors.HexColor("#4A5568")      # Dark Grey Contact Info
    
    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=PRIMARY_COLOR,
        fontName='Helvetica-Bold'
    )
    
    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=MUTED_TEXT,
        fontName='Helvetica'
    )
    
    section_heading = ParagraphStyle(
        'ResumeSectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=SECONDARY_COLOR,
        fontName='Helvetica-Bold',
        spaceBefore=14,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=TEXT_COLOR,
        fontName='Helvetica',
        spaceAfter=6
    )
    
    # 4. Construct Header Block (Side-by-side using Table)
    header_text_nodes = [
        Paragraph(name, title_style),
        Spacer(1, 4),
        Paragraph(f"Email: {email}   |   Mobile: {phone}", contact_style)
    ]
    
    # Process profile image wrapper safely if provided
    profile_img = None
    if image_bytes:
        try:
            image_stream = io.BytesIO(image_bytes)
            # Create a 75x75 points profile avatar box
            profile_img = Image(image_stream, width=75, height=75)
        except Exception:
            profile_img = Paragraph("<b style='color:red;'>[Image Error]</b>", contact_style)
    else:
        # Graceful placeholder styling fallback if no image upload exists
        profile_img = Paragraph("<i>No Image</i>", contact_style)
        
    # Header Grid: 430 points for Left info column, 100 points for Right photo cell
    header_table = Table([[header_text_nodes, profile_img]], colWidths=[430, 100])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    
    # Horizontal rule separator banner accent lines
    divider = Table([['']], colWidths=[532], rowHeights=[1])
    divider.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SECONDARY_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(Spacer(1, 10))
    story.append(divider)
    story.append(Spacer(1, 10))
    
    # 5. Helper function to create clean structured layout segments
    def add_section(title: str, content: str):
        if content.strip():
            story.append(Paragraph(title, section_heading))
            # Normalize user newlines into crisp ReportLab paragraph flow breaks
            formatted_text = content.replace("\n", "<br/>")
            story.append(Paragraph(formatted_text, body_style))
            
    # 6. Append Sections Sequentially
    add_section("Professional Summary", summary)
    add_section("Qualification", qualification)
    add_section("Experience", experience)
    add_section("Skills", skills)
    add_section("projects",projects)
    add_section("research_works", research_works)
    
    # 7. Document Final Compilation Build Assembly 
    doc.build(story)
    buffer.seek(0)
    return buffer

@app.post("/generate-resume")
async def generate_resume_endpoint(
    name: str = Form(..., description="Full Name"),
    phone: str = Form(..., description="Mobile / Telephone number"),
    email: str = Form(..., description="Email address"),
    professional_summary: str = Form(..., description="Brief profile introduction"),
    qualification: str = Form(..., description="Academic background"),
    experience: str = Form(..., description="Work history details"),
    skills: str = Form(..., description="Technical or professional competencies"),
    projects:str = Form(..., description ="Projects Details"),
    research_works:str = Form(..., description ="Research Work Details"),
    profile_image: Optional[UploadFile] = File(None, description="Optional profile photo image file upload")
):
    # Form input schema format validation checks
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="Invalid email address format standard.")
        
    image_data = None
    if profile_image:
        # Validate that the uploaded item presents a valid image signature format
        if not profile_image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file file stream must be a valid image type formatting.")
        image_data = await profile_image.read()
        
    try:
        pdf_stream = build_pdf_stream(
            name=name,
            phone=phone,
            email=email,
            summary=professional_summary,
            qualification=qualification,
            experience=experience,
            skills=skills,
            projects =projects, 
            research_works= research_works ,
            image_bytes=image_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate layout file data compilation downstream error: {str(e)}")
        
    # Generate clean filesystem compatible safe export naming strings
    filename_clean = "".join([c for c in name if c.isalpha() or c.isspace()]).strip().replace(" ", "_")
    if not filename_clean:
        filename_clean = "Generated"
        
    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename_clean}_Resume.pdf"
        }
    )

if __name__ == "__main__":
   
    # Start production engine local serving instance loop configurations
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

