from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Sample data
sample_textbooks = [
    {"grade": "Grade 10", "subject": "Physics", "curriculum": "IB", "content": "Content for Grade 10 Physics IB"},
    {"grade": "Grade 11", "subject": "Math", "curriculum": "AP", "content": "Content for Grade 11 Math AP"},
    {"grade": "Grade 12", "subject": "Chemistry", "curriculum": "National Standard", "content": "Content for Grade 12 Chemistry National Standard"},
]

# Populate the database
def init_db():
    db = SessionLocal()
    for textbook in sample_textbooks:
        db.add(models.Textbook(**textbook))
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()