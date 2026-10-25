import io
import re
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

# ReportLab components
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI(title="Professional Resume Generator")

def build_pdf_stream(
    name: str,
    phone: str,
    email: str,
    summary: str,
    qualification: str,
    experience: str,
    projects: str,     # Added
    research_works: str,     # Added
    skills: str,
    image_bytes: Optional[bytes] = None
) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        leftMargin=40, 
        rightMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()
    
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
    
    # Header Setup
    header_text_nodes = [
        Paragraph(name, title_style),
        Spacer(1, 4),
        Paragraph(f"Email: {email}   |   Mobile: {phone}", contact_style)
    ]
    
    profile_img = None
    if image_bytes:
        try:
            image_stream = io.BytesIO(image_bytes)
            profile_img = Image(image_stream, width=75, height=75)
        except Exception:
            profile_img = Paragraph("<b style='color:red;'>[Image Error]</b>", contact_style)
    else:
        profile_img = Paragraph("<i>No Image</i>", contact_style)
        
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
    
    # Colored structural line
    divider = Table([['']], colWidths=[532], rowHeights=[2])
    divider.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SECONDARY_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(Spacer(1, 10))
    story.append(divider)
    story.append(Spacer(1, 10))
    
    # Helper to append sections
    def add_section(title: str, content: str):
        if content and content.strip():
            story.append(Paragraph(title, section_heading))
            formatted_text = content.replace("\n", "<br/>")
            story.append(Paragraph(formatted_text, body_style))
            
    # Compile ReportLab elements sequentially
    add_section("Professional Summary", summary)
    add_section("Qualification", qualification)
    add_section("Experience", experience)
    add_section("Project Works", projects)     # Added to PDF
    add_section("Research Works", research_works)    # Added to PDF
    add_section("Skills", skills)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

@app.get("/", response_class=HTMLResponse)
async def get_form():
    # Pure inline HTML/CSS styling container framework
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Professional Resume Generator</title>
        <style>
            body { font-family: sans-serif; background-color: #f4f7f6; padding: 20px; color: #333; }
            .card { max-width: 650px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
            h2 { color: #1a365d; text-align: center; margin-bottom: 5px; }
            p.sub { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
            .row { display: flex; gap: 15px; margin-bottom: 15px; }
            .col { flex: 1; display: flex; flex-direction: column; }
            label { font-weight: bold; font-size: 13px; margin-bottom: 5px; color: #444; }
            input, textarea { padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; width: 100%; box-sizing: border-box; }
            textarea { resize: vertical; }
            .full { margin-bottom: 15px; display: flex; flex-direction: column; }
            .btn { background: #1a365d; color: white; padding: 12px; border: none; width: 100%; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; }
            .btn:hover { background: #2b6cb0; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📄 Resume PDF Generator</h2>
            <p class="sub">Enter your details down below to compile your resume instantly.</p>
            
            <form action="/generate-resume" method="post" enctype="multipart/form-data">
                <div class="row">
                    <div class="col">
                        <label>Full Name</label>
                        <input type="text" name="name" required>
                    </div>
                    <div class="col">
                        <label>Mobile Number</label>
                        <input type="tel" name="phone" required>
                    </div>
                </div>
                
                <div class="full">
                    <label>Email Address</label>
                    <input type="email" name="email" required>
                </div>

                <div class="full">
                    <label>Profile Image</label>
                    <input type="file" name="profile_image" accept="image/*">
                </div>

                <div class="full">
                    <label>Professional Summary</label>
                    <textarea name="professional_summary" rows="3" required></textarea>
                </div>

                <div class="full">
                    <label>Qualification</label>
                    <textarea name="qualification" rows="3" placeholder="Degrees, institutions, years..." required></textarea>
                </div>

                <div class="full">
                    <label>Experience</label>
                    <textarea name="experience" rows="3" placeholder="Previous job descriptions..." required></textarea>
                </div>

                <div class="full">
                    <label>Project Works</label>
                    <textarea name="projects" rows="4"placeholder="Describe key projects, technologies used..." required></textarea>
                </div>

                <div class="full">
                    <label>Research Works</label>
                    <textarea name="research_works" rows="4" placeholder="Publications, thesis titles, research areas..." required></textarea>
                </div>

                <div class="full">
                    <label>Skills</label>
                    <textarea name="skills" rows="3" placeholder="e.g. Python, SQL, Project Management..." required></textarea>
                </div>

                <button type="submit" class="btn">⚡ Generate Resume PDF</button>
            </form>
        </div>
    </body>
    </html>
   """

@app.post("/generate-resume")
async def generate_resume_endpoint(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    professional_summary: str = Form(...),
    qualification: str = Form(...),
    experience: str = Form(...),
    projects: str = Form(...),  
    research_works: str = Form(...),  
    skills: str = Form(...),
    profile_image: Optional[UploadFile] = File(None)
):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="Invalid email format.")
        
    image_data = None
    if profile_image and profile_image.filename:
        if not profile_image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
        image_data = await profile_image.read()
        
    try:
        pdf_stream = build_pdf_stream(
            name=name, phone=phone, email=email, summary=professional_summary,
            qualification=qualification, experience=experience, projects=projects,
            research_works=research_works, skills=skills, image_bytes=image_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
        
    filename_clean = "".join([c for c in name if c.isalpha() or c.isspace()]).strip().replace(" ", "_")
    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename_clean}_Resume.pdf"
        }
    )

if __name__ == "__main__":
    import uvicorn
    # Start production engine local serving instance loop configurations
    uvicorn.run("main01:app", host="127.0.0.1", port=9000, reload=False)


