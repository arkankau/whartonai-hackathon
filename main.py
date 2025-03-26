from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

client = OpenAI(api_key=api_key)

app = FastAPI()

# Load the NLP model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the request model
class PDFRequest(BaseModel):
    grade: str
    subject: str
    curriculum: str
    topic: str

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Endpoint to handle form submissions
@app.post("/generate-pdf/")
async def generate_pdf(request: PDFRequest):
    try:
        # Fetch material slides
        material_slides = fetch_material_slides(request)
        
        # Fetch practice problems
        practice_problems = fetch_practice_problems(request)
        
        # Fetch references
        references = fetch_references(request)
        
        # Generate PDF
        pdf_path = create_pdf(request, material_slides, practice_problems, references)
        
        return {"pdf_path": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def match_content(request: PDFRequest):
    db = SessionLocal()
    content = db.query(models.Textbook).filter_by(
        grade=request.grade, subject=request.subject, curriculum=request.curriculum
    ).all()
    db.close()
    if content:
        combined_content = "\n\n".join([c.content for c in content])
        return combined_content, "No practice problems provided.", "No references provided."
    else:
        # If no content is found in the database, use the LLM to fetch information from the internet
        return fetch_content_from_llm(request)

def fetch_material_slides(request: PDFRequest):
    prompt = f"Provide detailed, structured material slides for {request.grade} {request.subject} on {request.topic} according to the {request.curriculum} curriculum. Avoid introductory phrases and focus on clear, concise content."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    material_slides = response.choices[0].message.content.strip()
    return material_slides

def fetch_practice_problems(request: PDFRequest):
    prompt = f"Generate practice problems and their solutions for {request.grade} {request.subject} on {request.topic} according to the {request.curriculum} curriculum. Avoid introductory phrases and focus on clear, concise content."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    practice_problems = response.choices[0].message.content.strip()
    return practice_problems

def fetch_references(request: PDFRequest):
    prompt = f"Provide references used for generating content for {request.grade} {request.subject} on {request.topic} according to the {request.curriculum} curriculum. Avoid introductory phrases and focus on clear, concise content."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    references = response.choices[0].message.content.strip()
    return references



def create_pdf(request: PDFRequest, material_slides: str, practice_problems: str, references: str):
    pdf_path = f"{request.grade}_{request.subject}_{request.topic}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Cover Page
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, f"{request.grade} {request.subject}: {request.topic}")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Curriculum: {request.curriculum}")
    c.showPage()
    
    # Material Slides
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Material Slides")
    c.setFont("Helvetica", 12)
    y_position = 730
    for line in material_slides.split('\n'):
        if y_position < 50:
            c.showPage()
            y_position = 750
        c.drawString(100, y_position, line)
        y_position -= 20
    c.showPage()
    
    # Practice Problems
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Practice Problems")
    c.setFont("Helvetica", 12)
    y_position = 730
    for line in practice_problems.split('\n'):
        if y_position < 50:
            c.showPage()
            y_position = 750
        c.drawString(100, y_position, line)
        y_position -= 20
    c.showPage()
    
    # References
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "References")
    c.setFont("Helvetica", 12)
    y_position = 730
    for line in references.split('\n'):
        if y_position < 50:
            c.showPage()
            y_position = 750
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.save()
    return pdf_path

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
