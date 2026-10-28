import secrets
import string
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, URL

app = FastAPI(title="URL Shortener API")

class URLRequest(BaseModel):
    url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_code(length=7):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

@app.get("/")
def home():
    return {"message": "URL Shortener API is running"}

@app.post("/shorten")
def shorten_url(data: URLRequest, request: Request, db: Session = Depends(get_db)):
    code = generate_code()
    while db.query(URL).filter(URL.short_code == code).first():
        code = generate_code()

    record = URL(original_url=str(data.url), short_code=code)
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "original_url": record.original_url,
        "short_url": str(request.base_url) + code,
        "short_code": code
    }

@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    records = db.query(URL).all()

    return [
        {
            "short_code": record.short_code,
            "original_url": record.original_url,
            "clicks": record.clicks,
            "created_at": record.created_at
        }
        for record in records
    ]

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    record = db.query(URL).filter(URL.short_code == short_code).first()

    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    record.clicks += 1
    db.commit()

    return RedirectResponse(url=record.original_url)